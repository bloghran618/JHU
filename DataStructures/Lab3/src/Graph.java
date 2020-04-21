 /*
  * This class stores information about the connectivity of the graph
  */

 public class Graph
{
    private int numNodes;
    private Neighbors[] nodes;

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
            this.nodes = new Neighbors[numNodes];

            for(int i = 0; i < numNodes; i++)
            {
                this.nodes[i] = new Neighbors();
            }
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

        for(int i = 0; i < this.numNodes; i++)
        {
            if(adjListBinary[i] == 0)
            {
                // do nothing;
            }
            else if(adjListBinary[i] == 1)
            {
                // add neighbor to node
                this.nodes[node].add(i);
            }
            else
            {
                throw new RuntimeException("Non-binary value in adj list");
            }
        }
    }

    /**
     * Converts the graphs to a string for output
     *
     * @return the string representing the graph
     */
    public String getGraphString()
    {
        String returnString = "";

        int isNeighbor = 0;

        returnString += "Size: " + this.numNodes + "\n";

        returnString += "Binary Implementation (mirror input):\n";
        for(int i = 0; i < this.numNodes; i++)
        {
            returnString += this.nodes[i].toBinaryString(this.numNodes) + "\n";
        }

        returnString += "Linked Implementation:\n";
        for(int i = 0; i < this.numNodes; i++)
        {
            returnString += "Node " + i + " Neighbors: ";
            returnString += this.nodes[i].toString() + "\n";
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
     * @param nodes the adjacency list
     */
    public void setNodes(Neighbors[] nodes)
    {
        this.nodes = nodes;
    }

    /**
     * Gets the graph adjacency list
     *
     * @return the adjacency list
     */
    public Neighbors[] getNodes()
    {
        return this.nodes;
    }

}
