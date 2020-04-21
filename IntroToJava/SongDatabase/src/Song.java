 /**
  * This class is used to represent a song
  *
  * @author Brian Loughran
  */

public class Song
{
    private String title;
    private String itemCode;
    private String description;
    private String artist;
    private String album;
    private double price;

    /**
     * Initialize the Song object
     *
     * @param title is the title of the song
     * @param itemCode is the item code for the song
     * @param description is a short description for the song
     * @param artist is the artist of the song
     * @param album is the album that the song is a part of
     * @param price is the price for the song
     */
    public Song(String title, String itemCode, String description,
                            String artist, String album, double price)
    {
        if(title.equals(""))
        {
            throw new RuntimeException("Title cannot be blank");
        }
        else if(title.contains(","))
        {
            throw new RuntimeException("Title cannot contain ','");
        }
        else if(itemCode.equals(""))
        {
            throw new RuntimeException("Item Code cannot be blank");
        }
        else if(itemCode.contains(","))
        {
            throw new RuntimeException("Item Code cannot contain ','");
        }
        else if(description.equals(""))
        {
            throw new RuntimeException("Description cannot be blank");
        }
        else if(description.contains(","))
        {
            throw new RuntimeException("Description cannot contain ','");
        }
        else if(artist.equals(""))
        {
            throw new RuntimeException("Artist cannot be blank");
        }
        else if(artist.contains(","))
        {
            throw new RuntimeException("Artist cannot contain ','");
        }
        else if(album.equals(""))
        {
            throw new RuntimeException("Album cannot be blank");
        }
        else if(album.contains(","))
        {
            throw new RuntimeException("Album cannot contain ','");
        }
        else if(price < 0)
        {
            throw new RuntimeException("Price cannot be negative");
        }
        else
        {
            this.title = title;
            this.itemCode = itemCode;
            this.description = description;
            this.artist = artist;
            this.album = album;
            this.price = price;
        }
    }

    /**
     * Get a line that can be easily exported to .csv format
     *
     * @return the line to be sent to .csv
     */
    public String getCsvLine()
    {
        return String.format("%s,%s,%s,%s,%s,%.2f", this.title, this.itemCode,
                this.description, this.artist, this.album, this.price);
    }


    /**
     * Set title variable
     *
     * @param title the title of the song
     */
    public void setTitle(String title)
    {
        this.title = title;
    }

    /**
     * Get title variable
     *
     * @return the title
     */
    public String getTitle()
    {
        return this.title;
    }

    /**
     * Set itemCode variable
     *
     * @param itemCode the title of the song
     */
    public void setItemCode(String itemCode)
    {
        this.itemCode = itemCode;
    }

    /**
     * Get itemCode variable
     *
     * @return the item code
     */
    public String getItemCode()
    {
        return this.itemCode;
    }

    /**
     * Set description variable
     *
     * @param description the title of the song
     */
    public void setDescription(String description)
    {
        this.description = description;
    }

    /**
     * Get description variable
     *
     * @return the description
     */
    public String getDescription()
    {
        return this.description;
    }

    /**
     * Set artist variable
     *
     * @param artist the title of the song
     */
    public void setArtist(String artist)
    {
        this.artist = artist;
    }

    /**
     * Get artist variable
     *
     * @return the artist
     */
    public String getArtist()
    {
        return this.artist;
    }

    /**
     * Set album variable
     *
     * @param album the title of the song
     */
    public void setAlbum(String album)
    {
        this.album = album;
    }

    /**
     * Get album variable
     *
     * @return the album
     */
    public String getAlbum()
    {
        return this.album;
    }

    /**
     * Set price variable
     *
     * @param price the title of the song
     */
    public void setPrice(double price)
    {
        this.price = price;
    }

    /**
     * Get price variable
     *
     * @return the price
     */
    public double getPrice()
    {
        return this.price;
    }

    /**
     * return the price as a string (useful for setting text fields)
     *
     * @return the price as a string
     */
    public String getPriceString()
    {
        return String.format("%.2f", this.price);
    }
}