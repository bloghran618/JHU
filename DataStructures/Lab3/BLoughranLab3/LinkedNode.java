/*
 * This class one node in a linked list of neighbors
 */

public class LinkedNode
{
    private LinkedNode next;
    private int neighbor; // the node number of the neighbor node

    /**
     * Initializer for object of type LinkedNode
     *
     * @param neighbor the index of the neighbor
     */
    LinkedNode(int neighbor)
    {
        if(neighbor < 0)
        {
            throw new RuntimeException("Neighbor must have positive index");
        }
        else
            {
            this.next = null;
            this.neighbor = neighbor;
        }
    }

    /**
     * get the index of the neighbor
     *
     * @return the index of the neighbor
     */
    public int getNeighbor()
    {
        return this.neighbor;
    }

    /**
     * Sets the index of the neighbor
     *
     * @param neighbor the index of the neighbor
     */
    public void setNeighbor(int neighbor)
    {
        this.neighbor = neighbor;
    }

    /**
     * get the next LinkedNode in the linked list of neighbors
     *
     * @return the next LinkedNode
     */
    public LinkedNode getNext()
    {
        return next;
    }

    /**
     * Sets the next LinkedNode in the linked list of neighbors
     *
     * @param next the next LinkedNode
     */
    public void setNext(LinkedNode next)
    {
        this.next = next;
    }
}
