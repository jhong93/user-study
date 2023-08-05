
Set up the experiment. Define the mode (rate or compare). List out treatments.

```
./prepare.py --mode rate -ref ~/Desktop/autocompose/export_portrait_real_labeled/rgb -o work_dir/portrait \
    CACNet ~/Desktop/autocompose/export_portrait_real_labeled/user-study/CACNet/crops \
    HCIC ~/Desktop/autocompose/export_portrait_real_labeled/user-study/HCIC_CPC/crops \
    VFN ~/Desktop/autocompose/export_portrait_real_labeled/user-study/VFN/crops \
    GenCrop ~/Desktop/autocompose/export_portrait_real_labeled/user-study/GenCrop \
    GenCrop-C ~/Desktop/autocompose/export_portrait_real_labeled/user-study/GenCrop-C
```

Run the server.

```
./serve.py work_dir/portrait
```
