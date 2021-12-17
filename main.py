from PIL import Image, ImageFilter
import torch
import cv2 as cv
import torchvision.transforms as transform
import matplotlib.pyplot as plt
import os

# loader使用torchvision中自带的transforms函数
loader = transform.Compose([
    transform.ToTensor()])

unloader = transform.ToPILImage()


def save_image(tensor, **para):
    dir = 'results'
    image = tensor.cpu().clone()  # we clone the tensor to not do changes on it
    image = image.squeeze(0)  # remove the fake batch dimension
    image = unloader(image)
    image.save('results/{}.jpg'.format(1))


# 输入图片地址
# 返回tensor变量
def image_loader(image_name):
    image = Image.open(image_name).convert('RGB')
    image = loader(image).unsqueeze(0)
    return image.to(torch.float)


# 输入tensor变量
# 输出PIL格式图片
def tensor_to_PIL(tensor):
    image = tensor.cpu().clone()
    image = image.squeeze(0)
    image = unloader(image)
    return image


def imshow(tensor, title=None):
    image = tensor.cpu().clone()  # we clone the tensor to not do changes on it
    image = image.squeeze(0)  # remove the fake batch dimension
    image = unloader(image)

    plt.imshow(image)
    if title is not None:
        plt.title(title)
    plt.savefig("blur3.png", bbox_inches='tight')
    plt.show()  # pause a bit so that plots are updated


def gopro():
    img_path = "out/image1.jpg"
    image = image_loader(img_path)
    image = torch.mul(image, image)
    image_final = image
    sum = 1
    for i in range(2, 70):
        img_path = "out/image{}.jpg".format(i)
        image = image_loader(img_path)
        image = torch.mul(image, image)
        image_final += image
        sum += 1
    image_final = image_final / sum
    print(image_final.shape)
    save_image(image_final)
    print("success")


def main():
    img = Image.open('000047.png')
    blur_image = img.filter(ImageFilter.GaussianBlur(3))  # 模糊半径3
    blur_image.save("blur_img.png", quality=100)
    print("success")


if __name__ == "__main__":
    gopro()
    pass
