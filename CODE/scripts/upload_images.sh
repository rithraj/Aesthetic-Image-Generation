#!/bin/bash
for i in {1..100}; do
    gsutil -m cp -r $i 'gs://diffusiondb-images/'
done
