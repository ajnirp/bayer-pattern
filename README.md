Bayer Pattern, Computer Vision Fall 2017
--------

Rohan Prinja, rohan@cs.unc.edu, PID 730110583

Link to code
------

In my Github repo: https://github.com/ajnirp/bayer-pattern

Outputs
----

* The original image is `crayons.jpg`
* The demosaiced image is `demosaiced.jpg`. Note that it contains some additional artifacts induced by converting to JPG. Matplotlib does not render to BMP, so to see the "correct" reconstructed image, please run the code.
* The image displaying the artifacts is `artif.png`.
* The error map is `err.png`

Images
----

![](https://i.imgur.com/A8f8Uwj.jpg)
*Original image (above)*


![](https://i.imgur.com/rM7HYu9.png)
*Reconstructed image (above)*

Error values
----

Maximum pixel error: `118370.125`

Average pixel error: `41189.031`

Error Visualisation
-----------

![](https://i.imgur.com/wBIaBE5.png)
*Error map (above)*

To best visualize the error, I took the `log` of the error map (base 2) to bring the errors into a more manageable space. As we can see from the error map, the errors are greatest at edges within the image, such as shadows on the surfaces of the crayons, or the tips of the crayons.


Artifacts
-----

![](https://i.imgur.com/L6Udu9I.png)
*Region with high artifacts (above)*

We can see ringing artifacts on the left edge of the tip of the yellow crayon, such as small patches of blue pixels. In general, images reconstructed by demosaicing will exhibit such ringing artifacts at edges, where there is a sharp intensity change. The blue pixels appearing are an example of **false color**. There is an abrupt change in intensity in the green and blue channels along the edge of the yellow crayon's tip. However, in the red color channel, the change in intensity is not so large. This inconsistency between the three color channels is what leads to the formation of false color values like the blue pixels we see in the reconstructed image.
