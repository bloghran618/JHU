 /*
  * This class stores information about the connectivity of the graph
  */

public class Graph
{
    private int numNodes;
    private boolean[][] adjList;

    /**
     * Graphs initializer initializes an empty graph of size numNodes
     *
     * @param numNodes is the number of nodes
     */
    Graph(int numNodes)
    {
        if(numNodes < 1)
        {
            throw new RuntimeException("Number of nodes must be positive");
        }
        else
        {
            this.numNodes = numNodes;
            this.adjList = new boolean[numNodes][numNodes];
        }
    }

    /**
     * Adds an adjacency list for a single node
     *
     * @param node the node to add the adj list to
     * @param adjListBinary a binary list of adjacencies to add to the node
     */
    public void addAdjListAtNode(int node, int[] adjListBinary)
    {
        // check the adjacency list the correct length
        if(adjListBinary.length != this.numNodes)
        {
            throw new RuntimeException("Incorrect length for adjacency list");
        }

        boolean[] adjListBool = new boolean[this.numNodes];

        for(int i = 0; i < this.numNodes; i++)
        {
            if(adjListBinary[i] == 0)
            {
                adjListBool[i] = false;
            }
            else if(adjListBinary[i] == 1)
            {
                adjListBool[i] = true;
            }
            else
            {
                throw new RuntimeException("Non-binary value in adj list");
            }
        }

        this.adjList[node] = adjListBool;
    }


    /**
     * Converts the graphs to a string for output
     *
     * @return the string representing the graph
     */
    public String getGraphString()
    {
        String returnString = "";

        int trueOrFalse = 0;

        returnString += "Size: " + this.numNodes + "\n";

        for(int i = 0; i < this.numNodes; i++)
        {
            returnString += "[";
            for(int j = 0; j < this.numNodes; j++)
            {
                // convert true/false to 1/0
                if(this.adjList[i][j])
                {
                    trueOrFalse = 1;
                }
                else
                {
                    trueOrFalse = 0;
                }
                returnString += trueOrFalse + ", ";
            }

            if(!returnString.equals("["))
            {
                // crop off the last ", " in the list if not empty
                returnString = returnString.substring(0,
                        returnString.length() - 2);
            }

            returnString += "]\n";
        }
        return returnString;
    }

    /**
     * Sets the number of nodes
     *
     * @param numNodes the number of nodes
     */
    public void setNumNodes(int numNodes)
    {
        this.numNodes = numNodes;
    }

    /**
     * Gets the number of nodes
     *
     * @return the number of nodes
     */
    public int getNumNodes()
    {
        return this.numNodes;
    }

    /**
     * Sets the graph adjacency list
     *
     * @param adjList the adjacency list
     */
    public void setAdjList(boolean[][] adjList)
    {
        this.adjList = adjList;
    }

    /**
     * Gets the graph adjacency list
     *
     * @return the adjacency list
     */
    public boolean[][] getAdjList()
    {
        return this.adjList;
    }
}
