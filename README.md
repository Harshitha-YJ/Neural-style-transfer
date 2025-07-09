# 🎨 Neural Style Transfer

A Python-based program that applies the artistic style of one image (e.g., a painting) to another image (e.g., a photograph), using a pre-trained VGG19 deep learning model.

---

## 📌 Features

* Transfer artistic style from one image to another
* Uses **VGG19** pre-trained model from PyTorch
* Supports any `.jpg`, `.png`, etc. content and style images
* Saves the output image and shows a live preview

---

## 🖼️ Example

> Content Image + Style Image → Stylized Output
# 🎨 Neural Style Transfer

A Python-based program that applies the artistic style of one image (e.g., a painting) to another image (e.g., a photograph), using a pre-trained VGG19 deep learning model.

---

## 📌 Features

* Transfer artistic style from one image to another
* Uses **VGG19** pre-trained model from PyTorch
* Supports any `.jpg`, `.png`, etc. content and style images
* Saves the output image and shows a live preview

---

## 🖼️ Example

> Content Image + Style Image → Stylized Output

---

## 🛠️ Requirements

* Python 3.7+
* pip installed packages:

  ```bash
  pip install torch torchvision matplotlib pillow
  ```

---

## 🚀 How to Use

1. Save your photo as `content.jpg` and your painting as `style.jpg`

2. Place them in the **same folder** as the script `neural_style_transfer.py`

3. Run the script:

   ```bash
   python neural_style_transfer.py
   ```

4. After a few moments, your styled image will be saved as:

   ```
   output.jpg
   ```

   ...and also displayed on-screen.

---

## 🧠 How It Works

* Loads content and style images
* Passes them through VGG19
* Optimizes a clone of the content image to match the style and content
* Uses Gram Matrix for style representation
* Combines both losses to generate the stylized image

---

## 🖼️ Configuration

You can customize these in the script:

```python
content_image_path = "content.jpg"
style_image_path = "style.jpg"
output_image_path = "output.jpg"
image_size = 512  # for GPU, use 256 for CPU if slow
```

---

## 💡 Notes

* The script downloads VGG19 weights automatically the first time
* Works on CPU and GPU (if available)
* Resize your images to the same size for best results

---

## 📄 License

Free and open-source under the MIT License.

---

## 👩‍💻 Author

Harshitha YJ | Powered by OpenAI's ChatGPT


---

## 🛠️ Requirements

* Python 3.7+
* pip installed packages:

  ```bash
  pip install torch torchvision matplotlib pillow
  ```

---

## 🚀 How to Use

1. Save your photo as `content.jpg` and your painting as `style.jpg`

2. Place them in the **same folder** as the script `neural_style_transfer.py`

3. Run the script:

   ```bash
   python neural_style_transfer.py
   ```

4. After a few moments, your styled image will be saved as:

   ```
   output.jpg
   ```

   ...and also displayed on-screen.

---

## 🧠 How It Works

* Loads content and style images
* Passes them through VGG19
* Optimizes a clone of the content image to match the style and content
* Uses Gram Matrix for style representation
* Combines both losses to generate the stylized image

---

## 🖼️ Configuration

You can customize these in the script:

```python
content_image_path = "content.jpg"
style_image_path = "style.jpg"
output_image_path = "output.jpg"
image_size = 512  # for GPU, use 256 for CPU if slow
```

---

## 💡 Notes

* The script downloads VGG19 weights automatically the first time
* Works on CPU and GPU (if available)
* Resize your images to the same size for best results

---

## 📄 License

Free and open-source under the MIT License.

---

## 👩‍💻 Author

Harshitha YJ | Powered by OpenAI's ChatGPT
