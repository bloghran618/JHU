/*
 / AllCapabiliitesObject can draw, rotate, resize and play sounds
 */

public interface AllCapabilitiesObject extends Drawable, Resizable,
        Rotatable, Sounds
{
    void drawObject();
    void resizeObject();
    void rotateObject();
    void playSound();
}
