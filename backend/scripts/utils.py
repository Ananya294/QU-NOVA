import matplotlib.pyplot as plt
from fpdf import FPDF
import os

def generate_pdf_report(volume, prediction, output_path): #vol -> 3d numpy array to rep mri scan, pred->segmentati0on mask from model, o/p path -> path to write final pdf
    img_vol = volume[..., 1] if volume.ndim == 4 else volume #handles both 3d and 4d vols, if 4d -> last channel reps modlaities or channels(t1,t2) extracts second modality(index 1) often t2 or flair

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="BraTS Segmentation Report", ln=True, align='C')

    steps = max(1, img_vol.shape[2] // 3)
    slice_idxs = list(range(0, img_vol.shape[2], steps))[:3]

    for i in slice_idxs:
        fig, axes = plt.subplots(1, 2, figsize=(8, 4))
        axes[0].imshow(img_vol[:, :, i], cmap='gray')
        axes[0].set_title("Input")
        axes[0].axis('off')

        axes[1].imshow(prediction[:, :, i], cmap='viridis')
        axes[1].set_title("Prediction")
        axes[1].axis('off')

        tmp = f"slice_{i}.png"
        fig.savefig(tmp, bbox_inches='tight')
        plt.close(fig)

        pdf.image(tmp, w=180)
        os.remove(tmp)

    pdf.output(output_path)
    return output_path