# Scene-Graph-For-Videos

Our KERN model is based on the [KERN](https://github.com/yuweihao/KERNk) but we have modified the code for our custom image. Look into our blog post for detailed changes. Our Caption_Model is based on the [text-summarization-tensorflow](https://github.com/dongjun-Lee/text-summarization-tensorflow).

# SetUp
First Setup the Kern according to the original website. 

Download the dataset from [charaders](http://vuchallenge.org/charades.html). Run the charaders_datamaker.py files to get the key frmaes from the videos.

Run Kern in sgdet mode by running the eval_kern_sgdet.sh file.

After getting .pkl files run the scene_grpah_aggregator.py file to get common scene grpah for each video.

Run the Caption_Model for training by running 

 ```$ python train.py```

For Testing 

```$ python test.py```

