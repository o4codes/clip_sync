import io
import qrcode


class QRCodeGenerator:
    def __init__(self, encode_data: str):
        self.encode_data = encode_data
        self._border_size = 4
        self._box_size = 10
        self._error_correction = qrcode.ERROR_CORRECT_M
        self._fill_color = "black"
        self._back_color = "white"
        self._output_format = "PNG"

    def make(self) -> io.BytesIO:
        qr = qrcode.QRCode(
            version=1,
            error_correction=self._error_correction,
            box_size=self._box_size,
            border=self._border_size,
        )
        qr.add_data(self.encode_data)
        qr.make(fit=True)
        qr_image = qr.make_image(
            fill_color=self._fill_color, back_color=self._back_color
        )
        byte_io = io.BytesIO()
        qr_image.save(byte_io, format=self._output_format)
        byte_io.seek(0)
        return byte_io
