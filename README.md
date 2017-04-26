# rakuten-font2char2word2sent2doc-experiment

Internal use only.


## Prerequisites

See [rakuten2json.rb](https://github.com/raviqqe/rakuten2json.rb).


## Training

To train a font2char2word2sent2doc model with a training dataset
evaluating with a validation dataset, run the following command.

```
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda CUDA_VISIBLE_DEVICES=$gpu_id rake train
```

`$gpu_id` is an integer indentifier of a GPU on your machine.
When it has 4 GPUs, `$gpu_id` should be in a range of 0 to 3.

When you stop training, you can restart it running the same command as above.


## Evaluation

To evaluate a font2char2word2sent2doc model with a evaluation dataset,
run the following command.
Note that TensorFlow v1.0.1 has
[an issue](https://github.com/tensorflow/tensorflow/issues/7407)
that `Estimator.evaluate()` does not catch `OutOfRangeError`.
You may need to specify an exact number of batches used for evaluation
via `--eval_step` flag in [Rakefile](Rakefile).

```
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda CUDA_VISIBLE_DEVICES=$gpu_id rake evaluate
```


## Using TensorBoard

At a top-level directory, run the following command.

```
tensorboard --logdir var/output --port 8888
```


## Visualization of font attentions

After training, run the following command.

```
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda CUDA_VISIBLE_DEVICES=$gpu_id rake visualize
```

You should see image files in `var/font_attentions`.


## Cleaning up

The command below cleans up everything like saved models, processed datasets
and etc.

```
rake clobber
```


## License

[The Unlicense](https://unlicense.org)
