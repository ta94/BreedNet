import torch
import torchvision

from breednet import BreedNet,model_size_estimater

#### dataset 
from SemCKD.dataset.cifar100 import get_cifar100_dataloaders, get_cifar100_dataloaders_sample

train_loader, val_loader = get_cifar100_dataloaders(batch_size=256,
                                                                num_workers=6)

### get input trained network
model = torchvision.models.mobilenet_v2(pretrained=False)
model.classifier[1]=torch.nn.Linear(in_features=1280, out_features=100, bias=True)
## cpu
#model.load_state_dict(torch.load('pretrained_models/mobilenetv2_cifar100-124-best.pth',map_location=torch.device("cpu")))
## gpu
model.load_state_dict(torch.load('pretrained_models/mobilenetv2_cifar100-124-best.pth'))

print("Size of Input net",model_size_estimater(model))

## breednet object creation
mobilenet_breednet = BreedNet(inp_net=model,redn_frac=0.75,gpu=True,train_epochs=1000,num_classes=100,input_size=(3,320,320))
print(mobilenet_breednet)

## trim input network
mobilenet_breednet.trim_net()
## the trimmed network is accessible using mobilenet_breednet.out_net

print("Size of trimmed net",model_size_estimater(mobilenet_breednet.out_net))

## train the trimmed network and 
## get best trimmed model and path of folder with best trimmed model torchscript and json with metrics information
net,torchscript_and_info_json_path = mobilenet_breednet.train(train_loader=train_loader,val_loader=val_loader)


