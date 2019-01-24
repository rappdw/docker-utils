#!/usr/bin/env bash

# update anaconda
echo "Updating Anaconda"
conda update -y -n base -c defaults conda

# remove the last lines of .profile, .dlamirc, and .zshrc which add anaconda/bin to the path,
# instead, we'll use "current" anaconda style of sourcing the profile
echo 'Converting to "modern" style conda'
sed -i '$ d' .profile
sed -i '$ d' .dlamirc
sed -i '$ d' .zshrc
echo ". /home/ubuntu/anaconda3/etc/profile.d/conda.sh" >> ~/.profile
echo "conda activate base" >> ~/.profile

# change the MOTD to reflect the "current style", e.g. conda source <env>
sudo sed -i 's/source activate/conda activate/g' /etc/update-motd.d/00-header
sudo sed -i 's/source activate/conda activate/g' /home/ubuntu/README

# remove the python2 environments...
conda env remove -y --name amazonei_mxnet_p27
conda env remove -y --name amazonei_tensorflow_p27
conda env remove -y --name caffe2_p27
conda env remove -y --name caffe_p27
conda env remove -y --name chainer_p27
conda env remove -y --name cntk_p27
conda env remove -y --name mxnet_p27
conda env remove -y --name python2
conda env remove -y --name pytorch_p27
conda env remove -y --name tensorflow_p27
conda env remove -y --name theano_p27

rm -rf /home/ubuntu/anaconda2

sudo sed -i '/amazonei_mxnet_p27/d' /etc/update-motd.d/00-header
sudo sed -i '/amazonei_tensorflow_p27/d' /etc/update-motd.d/00-header
sudo sed -i '/caffe2_p27/d' /etc/update-motd.d/00-header
sudo sed -i '/caffe_p27/d' /etc/update-motd.d/00-header
sudo sed -i '/chainer_p27/d' /etc/update-motd.d/00-header
sudo sed -i '/cntk_p27/d' /etc/update-motd.d/00-header
sudo sed -i '/mxnet_p27/d' /etc/update-motd.d/00-header
sudo sed -i '/python2/d' /etc/update-motd.d/00-header
sudo sed -i '/pytorch_p27/d' /etc/update-motd.d/00-header
sudo sed -i '/tensorflow_p27/d' /etc/update-motd.d/00-header
sudo sed -i '/theano_p27/d' /etc/update-motd.d/00-header

sudo sed -i '/amazonei_mxnet_p27/d' /home/ubuntu/README
sudo sed -i '/amazonei_tensorflow_p27/d' /home/ubuntu/README
sudo sed -i '/caffe2_p27/d' /home/ubuntu/README
sudo sed -i '/caffe_p27/d' /home/ubuntu/README
sudo sed -i '/chainer_p27/d' /home/ubuntu/README
sudo sed -i '/cntk_p27/d' /home/ubuntu/README
sudo sed -i '/mxnet_p27/d' /home/ubuntu/README
sudo sed -i '/python2/d' /home/ubuntu/README
sudo sed -i '/pytorch_p27/d' /home/ubuntu/README
sudo sed -i '/tensorflow_p27/d' /home/ubuntu/README
sudo sed -i '/theano_p27/d' /home/ubuntu/README
