# Task: Neural Style Transfer
# Apply artistic styles to photographs using a pre-trained model
# Deliverable: Python script that shows styled output images

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms, models
from PIL import Image
import matplotlib.pyplot as plt
import copy

# --- Configuration ---
content_image_path = "content.jpg"   # Replace with your content image path
style_image_path = "style.jpg"       # Replace with your style image path
output_image_path = "output.jpg"
image_size = 512 if torch.cuda.is_available() else 256

# --- Load Images ---
loader = transforms.Compose([
    transforms.Resize((image_size, image_size)),
    transforms.ToTensor()
])

def image_loader(image_name):
    image = Image.open(image_name).convert('RGB')
    image = loader(image).unsqueeze(0)
    return image.to(torch.float)

content_img = image_loader(content_image_path)
style_img = image_loader(style_image_path)
assert content_img.size() == style_img.size(), "Images must be the same size"

# --- Display helper ---
unloader = transforms.ToPILImage()
def imshow(tensor, title=None):
    image = tensor.cpu().clone().squeeze(0)
    image = unloader(image)
    plt.imshow(image)
    if title: plt.title(title)
    plt.pause(0.001)

# --- Content & Style Loss ---
class ContentLoss(nn.Module):
    def __init__(self, target):
        super(ContentLoss, self).__init__()
        self.target = target.detach()

    def forward(self, input):
        self.loss = nn.functional.mse_loss(input, self.target)
        return input

class StyleLoss(nn.Module):
    def __init__(self, target_feature):
        super(StyleLoss, self).__init__()
        self.target = self.gram_matrix(target_feature).detach()

    def gram_matrix(self, input):
        a, b, c, d = input.size()
        features = input.view(a * b, c * d)
        G = torch.mm(features, features.t())
        return G.div(a * b * c * d)

    def forward(self, input):
        G = self.gram_matrix(input)
        self.loss = nn.functional.mse_loss(G, self.target)
        return input

# --- Model Setup ---
vgg = models.vgg19(pretrained=True).features.eval()
cnn_normalization_mean = torch.tensor([0.485, 0.456, 0.406])
cnn_normalization_std = torch.tensor([0.229, 0.224, 0.225])

def get_style_model_and_losses(cnn, style_img, content_img):
    normalization = Normalization(cnn_normalization_mean, cnn_normalization_std)
    content_layers = ['conv_4']
    style_layers = ['conv_1', 'conv_2', 'conv_3', 'conv_4', 'conv_5']

    content_losses = []
    style_losses = []

    model = nn.Sequential(normalization)
    i = 0
    for layer in cnn.children():
        if isinstance(layer, nn.Conv2d):
            i += 1
            name = f'conv_{i}'
        elif isinstance(layer, nn.ReLU):
            name = f'relu_{i}'
            layer = nn.ReLU(inplace=False)
        elif isinstance(layer, nn.MaxPool2d):
            name = f'pool_{i}'
        elif isinstance(layer, nn.BatchNorm2d):
            name = f'bn_{i}'
        else:
            raise RuntimeError(f'Unrecognized layer: {layer.__class__.__name__}')

        model.add_module(name, layer)

        if name in content_layers:
            target = model(content_img).detach()
            content_loss = ContentLoss(target)
            model.add_module(f"content_loss_{i}", content_loss)
            content_losses.append(content_loss)

        if name in style_layers:
            target_feature = model(style_img).detach()
            style_loss = StyleLoss(target_feature)
            model.add_module(f"style_loss_{i}", style_loss)
            style_losses.append(style_loss)

    # Trim the model
    for i in range(len(model) - 1, -1, -1):
        if isinstance(model[i], (ContentLoss, StyleLoss)):
            break
    model = model[:i+1]

    return model, style_losses, content_losses

class Normalization(nn.Module):
    def __init__(self, mean, std):
        super(Normalization, self).__init__()
        self.mean = torch.tensor(mean).view(-1, 1, 1)
        self.std = torch.tensor(std).view(-1, 1, 1)

    def forward(self, img):
        return (img - self.mean) / self.std

# --- Style Transfer ---
input_img = content_img.clone()
model, style_losses, content_losses = get_style_model_and_losses(vgg, style_img, content_img)
optimizer = optim.LBFGS([input_img.requires_grad_()])

print("🖌️ Starting style transfer...")

epochs = 300
for epoch in range(epochs):
    def closure():
        input_img.data.clamp_(0, 1)
        optimizer.zero_grad()
        model(input_img)
        style_score = sum(sl.loss for sl in style_losses)
        content_score = sum(cl.loss for cl in content_losses)
        loss = style_score + content_score
        loss.backward()
        return loss

    optimizer.step(closure)
    if epoch % 50 == 0:
        print(f"Epoch {epoch}/{epochs} complete")

input_img.data.clamp_(0, 1)

# --- Save and show output ---
final_image = input_img.cpu().clone().squeeze(0)
final_image = unloader(final_image)
final_image.save(output_image_path)
print(f"✅ Style transfer complete. Output saved as {output_image_path}")
imshow(input_img, title="Styled Output")
