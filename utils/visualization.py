import matplotlib.pyplot as plt
import matplotlib.patches as patches

def plot_image_with_boxes(image, boxes, labels):
    """Plot image with bounding boxes and labels."""
    fig, ax = plt.subplots(1, figsize=(12, 9))
    ax.imshow(image)
    for box, label in zip(boxes, labels):
        rect = patches.Rectangle(
            (box[0], box[1]), box[2] - box[0], box[3] - box[1],
            linewidth=2, edgecolor='r', facecolor='none'
        )
        ax.add_patch(rect)
        plt.text(
            box[0], box[1], label, fontsize=12,
            bbox=dict(facecolor='yellow', alpha=0.5)
        )
    plt.show()

def generate_final_output(image, table_data, output_path):
    """Generate final output image with table of data."""
    fig, ax = plt.subplots(1, 2, figsize=(16, 9))
    ax[0].imshow(image)
    ax[0].axis('off')
    
    table = ax[1].table(
        cellText=table_data,
        colLabels=['Object ID', 'Description', 'Text Data', 'Attributes'],
        cellLoc='center',
        loc='center'
    )
    ax[1].axis('off')
    
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
