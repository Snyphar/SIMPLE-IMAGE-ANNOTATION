# Simple Image Annotation

## Overview
**Simple Image Annotation** is a Flet-based Python tool that simplifies the process of annotating images with bounding boxes for multiple labels. This tool allows you to annotate one image and apply those annotations to a batch of images, saving both the annotations and the original images in a specified directory.

## Features
- **Flet-Powered Interface**: A user-friendly graphical interface built with Flet, providing a smooth and intuitive annotation experience.
- **Bounding Box Annotation**: Annotate images with bounding boxes for multiple labels.
- **Batch Labeling**: Apply the same bounding box labels across multiple images automatically.
- **Directory Management**: Save annotated and raw images along with their corresponding annotation files in your desired directory.

## Installation
To install and run **Simple Image Annotation**, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/simple-image-annotation.git
    ```
2. Navigate to the project directory:
    ```bash
    cd simple-image-annotation
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the tool:
    ```bash
    python main.py
    ```

## Usage
1. Launch the tool by running `main.py`.
2. Load your images into the Flet interface.
3. Use the annotation tool to draw bounding boxes around objects in the first image and assign labels.
4. Automatically apply the same annotations to other images in your dataset.
5. Save the annotations and images to your desired directory.

## Directory Structure
After saving, your specified directory will contain:
- **Annotated Images**: Images with bounding boxes and labels overlaid.
- **Raw Images**: The original images without any modifications.
- **Annotations**: A CSV file containing the bounding box coordinates and labels.


## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have any ideas or improvements.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
For any questions or suggestions, please contact [snyphar.ex@gmail.com](snyphar.ex@gmail.com).

