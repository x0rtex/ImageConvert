import os
from PIL import Image


class ImageConverter:
    def __init__(self, directory, source_ext, target_ext, compression):
        """Initialize ImageConverter"""
        self.directory = directory
        self.source_ext = source_ext.lower().lstrip('.')
        self.target_ext = target_ext.lower().lstrip('.')
        self.compression = compression
        self.converted_files = []
        self.source_files = []
        self.target_format = None

    def convert(self):
        """Convert images in directory"""
        self.validate_directory()
        self._validate_formats()

        for root, _, files in os.walk(self.directory):
            for file in files:
                if self._is_source_file(file):
                    source_path = os.path.join(root, file)
                    self._process_file(source_path)

    def _is_source_file(self, filename):
        """Check if file matches source extension"""
        return filename.lower().endswith(f".{self.source_ext}")

    def _validate_formats(self):
        """Validate source/target formats against Pillow's capabilities"""
        # Validate source format (readable)
        if f".{self.source_ext}" not in Image.registered_extensions():
            raise ValueError(f"Unsupported source format: {self.source_ext}")

        # Validate target format (writable)
        target_ext_with_dot = f".{self.target_ext}"
        if target_ext_with_dot not in Image.registered_extensions():
            raise ValueError(f"Unsupported target format: {self.target_ext}")

        self.target_format = Image.registered_extensions()[target_ext_with_dot]

    def _process_file(self, source_path):
        """Handle individual file conversion"""
        target_path = self._get_target_path(source_path)

        try:
            with Image.open(source_path) as img:
                converted_img = self._handle_image_mode(img)
                converted_img.save(
                    target_path,
                    format=self.target_format,
                    quality=self.compression,
                    optimize=True,
                    **self._get_format_specific_options(img)
                )
            self._track_conversion(source_path, target_path)
        except Exception as e:
            raise RuntimeError(f"Failed to convert {source_path}: {str(e)}")

    @staticmethod
    def _get_format_specific_options(img):
        """Handle format-specific save options"""
        options = {}
        if img.format == 'JPEG':
            options['progressive'] = True
            options['exif'] = img.info.get('exif', b'')
        return options

    def _handle_image_mode(self, img):
        """Convert image modes for format compatibility"""
        if self.target_format == 'JPEG' and img.mode in ('RGBA', 'LA'):
            return img.convert('RGB')
        return img

    def _get_target_path(self, source_path):
        """Generate target path from source path"""
        base = os.path.splitext(os.path.basename(source_path))[0]
        return os.path.join(
            os.path.dirname(source_path),
            f"{base}.{self.target_ext}"
        )

    def _track_conversion(self, source_path, target_path):
        """Record conversion results"""
        self.converted_files.append(target_path)
        self.source_files.append(source_path)

    def validate_directory(self):
        """Validate directory exists"""
        if not os.path.isdir(self.directory):
            raise ValueError(f"Directory not found: {self.directory}")

    def delete_files(self, file_type='source'):
        """Delete files of specified type (source/converted)"""
        target_files = self.source_files if file_type == 'source' else self.converted_files
        success = 0

        for file_path in target_files:
            try:
                os.remove(file_path)
                success += 1
            except Exception as e:
                raise RuntimeError(f"Failed to delete {file_path}: {str(e)}")

        return success, len(target_files)

    @property
    def conversion_count(self):
        """Return number of converted files"""
        return len(self.converted_files)

    @property
    def source_count(self):
        """Return number of source files"""
        return len(self.source_files)