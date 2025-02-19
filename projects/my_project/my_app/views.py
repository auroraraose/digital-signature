from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import FileResponse

from my_project.settings import CERTIFICATE_PATH
from .forms import DocumentUploadForm
from .models import Document
from pyhanko.sign.signers import SimpleSigner
from pyhanko.sign.fields import SigFieldSpec
from pyhanko.sign.validation import validate_pdf_signature
from pyhanko.sign import sign_pdf
from io import BytesIO

def upload_pdf(request):
    if request.method == 'POST' and request.FILES['original_pdf']:
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the original PDF
            doc = form.save(commit=False)
            doc.user = request.user
            doc.save()

            # Perform digital signing after saving
            signed_pdf_path = sign_document(doc.original_pdf.path)

            # Update document record with signed PDF path
            doc.signed_pdf = signed_pdf_path
            doc.signature_status = 'signed'
            doc.signed_at = timezone.now()
            doc.save()

            # Return the signed PDF
            return FileResponse(open(signed_pdf_path, 'rb'), as_attachment=True)

    else:
        form = DocumentUploadForm()

    return render(request, 'upload_pdf.html', {'form': form})


# def sign_document(original_pdf_path):
#     # Load your signer certificate and private key here
#     signer = SimpleSigner.load_pkcs12(
#         pfx_file=CERTIFICATE_PATH, 
#         passphrase=b'password'
#     )

#     # Specify where to save the signed PDF
#     signed_pdf_path = f"media/documents/signed_pdfs/signed_{timezone.now().strftime('%Y%m%d%H%M%S')}.pdf"

#     # Sign the document
#     sign_pdf(
#         original_pdf_path,  # Input file
#         signed_pdf_path,  # Output file
#         signer=signer,  # Your signer
#         field_name="Signature1"  # Signature field name
#     )

#     return signed_pdf_path

def sign_document(original_pdf_path):
    # Load the signer credentials (use correct passphrase)
    signer = SimpleSigner.load_pkcs12(
        pfx_file='certs/certificate.p12',  # Path to your certificate.p12
        passphrase=b'your_passphrase'
    )

    # Create a signature field specification (this ensures the field exists)
    signature_field = SigFieldSpec(sig_field_name="Signature1")  # Name of the signature field

    # Specify where to save the signed PDF
    signed_pdf_path = f"media/documents/signed_pdfs/signed_{timezone.now().strftime('%Y%m%d%H%M%S')}.pdf"

    # Sign the PDF
    sign_pdf(
        original_pdf_path,  # Input PDF
        signed_pdf_path,     # Output PDF
        signer=signer,       # Signer object
        sig_field_spec=signature_field  # Signature field specification
    )

    return signed_pdf_path

