import os
import json
import cv2
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image

def generate_final_output(master_id, image_path):
    def load_combined_data(master_id):
        json_path = os.path.join('json_files', master_id, 'final_results.json')
        with open(json_path, 'r') as f:
            final_data = json.load(f)
        return final_data

    def load_image(image_path):
        img = cv2.imread(image_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img_rgb

    def create_summary_table(final_data):
        df = pd.DataFrame(final_data)
        df = df[['object_id', 'detected_objects', 'extracted_text', 'summary']]
        df['detected_objects'] = df['detected_objects'].apply(
            lambda x: ", ".join([f"{obj['label']} ({obj['confidence']:.2f})" for obj in x])
        )
        df['extracted_text'] = df['extracted_text'].apply(lambda x: x if x else "No text")
        df['summary'] = df['summary'].apply(lambda x: x if x else "No summary available")
        return df

    def plot_annotated_image(img, final_data):
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.imshow(img)
        ax.set_title("Original Image")

        ax.axis('off')
        return fig

    def plot_summary_table(summary_table):
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=summary_table.values, colLabels=summary_table.columns, cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.5, 2)  # Adjust scaling for better readability
        for i in range(len(summary_table.columns)):
            table.auto_set_column_width(i)
        for key, cell in table.get_celld().items():
            cell.set_edgecolor('black')
            if key[0] == 0:
                cell.set_text_props(weight='bold', fontsize=12)
            cell.set_fontsize(10)
        plt.subplots_adjust(left=0.2, right=0.8, top=0.8, bottom=0.2)
        return fig

    def save_fig_as_image(fig, path):
        fig.savefig(path, bbox_inches='tight')
        plt.close(fig)

    def concatenate_images(image_path1, image_path2, output_path):
        img1 = Image.open(image_path1)
        img2 = Image.open(image_path2)
        dst = Image.new('RGB', (img1.width + img2.width, max(img1.height, img2.height)))
        dst.paste(img1, (0, 0))
        dst.paste(img2, (img1.width, 0))
        dst.save(output_path)

    def save_final_output(master_id):
        output_dir = os.path.join('final_outputs', master_id)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        image_plot_path = os.path.join(output_dir, 'annotated_image.png')
        table_plot_path = os.path.join(output_dir, 'summary_table.png')
        final_output_path = os.path.join(output_dir, 'final_output.png')

        return image_plot_path, table_plot_path, final_output_path

    final_data = load_combined_data(master_id)
    original_image = load_image(image_path)
    summary_table = create_summary_table(final_data)

    fig_image = plot_annotated_image(original_image, final_data)
    fig_table = plot_summary_table(summary_table)

    image_plot_path, table_plot_path, final_output_path = save_final_output(master_id)

    save_fig_as_image(fig_image, image_plot_path)
    save_fig_as_image(fig_table, table_plot_path)

    concatenate_images(image_plot_path, table_plot_path, final_output_path)
    print(f"Final output saved to '{final_output_path}'.")

# Example usage
if __name__ == '__main__':
    generate_final_output('8fb16678-83cf-4daf-81bb-179bf7ef10a3', 'uploaded_images/images.jpg')
