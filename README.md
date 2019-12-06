# Scene-Graph-For-Videos

Our KERN model is based on the [KERN](https://github.com/yuweihao/KERN) but we have modified the code for our custom image. Look into our blog post for detailed changes. Our Caption_Model is based on the [text-summarization-tensorflow](https://github.com/dongjun-Lee/text-summarization-tensorflow).

# SetUp
- Setup KERN following intructions [here](https://github.com/yuweihao/KERN). It has to be accomodated to run on custom images(Mentioned in blog).
- Download the dataset from [charades](http://vuchallenge.org/charades.html) & run the charaders_datamaker.py files to get the key frmaes from the videos.

- This frames have to be placed inside the data directory of KERN.

- Run Kern in sgdet mode by running the eval_kern_sgdet.sh file.
      ```./scripts/eval_kern_sgdet.sh```

- You will get a pickle(.pkl) file containing scene graphs for all the image frames. Run the scene_graph_aggregator.py file to get a common scene graph for each video.

- Run the Caption_Model for training by running 

 ```$ python train.py```

For Testing 

```$ python test.py```

