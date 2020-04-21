/*
 * This class is a linked list of neighbors for a node in the graph
 */

import java.util.Arrays;

public class Neighbors
{
    private LinkedNode head;

    /**
     * Initializer for object of type node
     */
    Neighbors()
    {
        this.head = null;
    }

    /**
     * Adds a neighbor to the adjacency list of object Node
     *
     * @param neighbor the index of the neighbor
     */
    public void add(int neighbor)
    {
        // if head empty set to neighbor
        if(this.head == null)
        {
            this.head = new LinkedNode(neighbor);
        }
        else
        {
            LinkedNode tail = this.head;
            while (tail.getNext() != null) {
                tail = tail.getNext();
            }
            tail.setNext(new LinkedNode(neighbor));
        }
    }

    /**
     * Converts the linked list to an integer list
     * e.x.: [1, 4, 5]
     *
     * @return the linked list as an integer list
     */
    public int[] toList()
    {
        int size = 0;
        LinkedNode node = this.head;
        while(node != null)
        {
            size++; // get the size of the list
            node = node.getNext();
        }

        int[] adjList = new int[size];
        node = this.head;
        for(int i = 0; i < size; i++) // loop over elements in the list
        {
            adjList[i] = node.getNeighbor() + 1;
            node = node.getNext();
        }

        return adjList;
    }

    /**
     * Converts the linked list to a string
     * e.x.: "[1, 4, 5]"
     *
     * @return the linked list as a string
     */
    public String toString()
    {
        String returnString = "";

        LinkedNode node = this.head;
        returnString += "[";
        while(node != null)
        {
            returnString += node.getNeighbor() + 1;
            if(node.getNext() != null)
            {
                returnString += ", ";
            }
            node = node.getNext();
        }
        returnString += "]";
        return returnString;
    }

    /**
     * Converts the linked list to a binary array of given length
     * e.x.: "[0, 1, 0, 0, 1, 1, 0]"
     *
     * @param length the length
     *
     * @return a binary array representing the linked list
     */
    public int[] toBinaryArray(int length)
    {
        int[] binaryArray = new int[length];
        Arrays.fill(binaryArray, 0);

        LinkedNode node = this.head;
        while(node != null)
        {
            binaryArray[node.getNeighbor()] = 1;
            node = node.getNext();
        }

        return binaryArray;
    }

    /**
     * Converts the linked list to a binary string of given length
     *
     * @param length the length
     *
     * @return a binary string representing the linked list
     */
    public String toBinaryString(int length)
    {
        String returnString = "[";

        int[] array = this.toBinaryArray(length);

        for(int i = 0; i < array.length; i++)
        {
            returnString += array[i];
            if(i < array.length - 1)
            {
                returnString += ", ";
            }
        }
        returnString += "]";

        return returnString;
    }

    /**
     * Gets the next node in the linked list
     *
     * @param current the current node number
     *
     * @return the next LinkedNode object
     */
    public LinkedNode getNext(int current)
    {
        LinkedNode node = head;

        try
        {
            while(node.getNeighbor() != current)
            {
                node = node.getNext();
            }
            return node;
        }
        catch(NullPointerException npe)
        {
            return null;
        }
    }

    /**
     * Gets the head of the linked list
     *
     * @return the head of the linked list
     */
    public LinkedNode getHead()
    {
        return this.head;
    }

    /**
     * Sets the head of the linked list
     *
     * @param head the head of the list
     */
    public void setHead(LinkedNode head)
    {
        this.head = head;
    }
}
