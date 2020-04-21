 /*
  * This is a class which keeps track of the valid paths of the graph
  */

public class PathsString
{
    private String paths;

    /**
     * Paths initializer initializes paths to an empty string
     */
    PathsString()
    {
        this.paths = "";
    }

    /**
     * Get the paths
     *
     * @return the paths
     */
    public String getPaths()
    {
        if(this.paths.equals(""))
        {
            return "No Paths Found";
        }
        else
        {
            return this.paths;
        }
    }

    /**
     * Set the paths
     *
     * @param paths the paths
     */
    public void setPaths(String paths)
    {
        this.paths = paths;
    }

    /**
     * Append a path to the paths
     *
     * @param path the path to append
     */
    public void append(String path)
    {
        if(this.paths.equals(""))
        {
            this.paths += path;
        }
        else
        {
            this.paths += "\n" + path;
        }
    }

    /**
     * Clear all current paths
     */
    public void clear()
    {
        this.paths = "";
    }

    /**
     * Prints the paths
     */
    public void print()
    {
        if(this.paths.equals(""))
        {
            System.out.println("No Path Found");
        }
        else
        {
            System.out.println(this.paths);
        }
    }

    /**
     * Get the number of paths
     *
     * @return the number of paths
     */
    public int getNumPaths()
    {
        if(this.paths.equals(""))
        {
            return 0;
        }
        else
        {
            return this.paths.split("\n", -1).length;
        }
    }
}
