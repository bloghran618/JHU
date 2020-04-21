/*
 * Stores the array to sign in a linked list
 */

public class LinkedList
{
    private Node head;
    private int length;

    LinkedList()
    {
        this.head = null;
        this.length = 0;
    }

    // initialize LinkedList to another LinkedList (copy)
    LinkedList(LinkedList linked)
    {
        this.head = linked.getHead();
        Node currentPaste = this.head;
        Node currentCopy = linked.getHead();

        // copy the length
        this.length = linked.getLength();

        try
        {
            while(true)
            {
                // for each node paste into new list
                currentCopy = currentCopy.getNext();
                currentPaste.setNext(currentCopy);
                currentPaste = currentPaste.getNext();
            }
        }
        catch(NullPointerException npe)
        {
            // end of list, do nothing
        }
    }

    /**
     * Inserts a new node in order to the linked list
     *
     * @param val the value to insert
     */
    public void insert(int val)
    {
        Node node = new Node(val);

        // if list is empty, insert at head
        if(this.head == null)
        {
            this.head = node;
        }
        else
        {
            Node current = this.head;
            Node parent = null;
            try
            {
                while(val > current.getVal())
                {
                    // traverse to proper place in ordered list
                    parent = current;
                    current = current.getNext();
                }
                try
                {
                    // If predecessor and successor, insert in between
                    parent.setNext(node);
                    node.setNext(current);
                }
                catch(NullPointerException noParent)
                {
                    // Parent has not been set yet, insert at head
                    node.setNext(this.head);
                    this.head = node;
                }
            }
            catch(NullPointerException endOfList)
            {
                // Insert at the end of the linked list
                parent.setNext(node);
                node.setNext(null);
            }
        }

        // maintain the proper length of the list
        incLength();
    }

    /**
     * Adds a value to the end of the linked list
     *
     * @param value the value to be added
     */
    public void append(int value)
    {
        // if head empty set to neighbor
        if(this.head == null)
        {
            this.head = new Node(value);
        }
        else
        {
            // traverse to tail and place node there
            Node tail = this.head;
            while (tail.getNext() != null) {
                tail = tail.getNext();
            }
            tail.setNext(new Node(value));
        }

        // maintain the proper length of the list
        incLength();
    }

    /**
     * Append a linked list to the end of the linked list
     * (Node that this method will not increment the length of the list)
     *
     * @param linkedList the linked list to append
     */
    public void appendList(LinkedList linkedList)
    {
        // if head empty set to neighbor
        if(this.head == null)
        {
            this.head = linkedList.getHead();
        }
        else
        {
            // traverse to tail and append list there
            Node tail = this.head;
            while (tail.getNext() != null) {
                tail = tail.getNext();
            }
            tail.setNext(linkedList.getHead());
        }

        this.length += linkedList.getLength();
    }

    /**
     * Converts the linked list to a string
     * Goes to newline every 15 values for readability
     * e.x.: "[1, 4, 5]"
     *
     * @return the linked list as a string
     */
    public String toString()
    {
        String returnString = "";
        int counter = 0;

        Node node = this.head;
        returnString += "[";
        while(node != null)
        {
            if(counter >= 10)
            {
                // indent every 10 items
                returnString += "\n";
                counter = 0;
            }

            // add value to returnString
            returnString += node.getVal();
            if(node.getNext() != null)
            {
                returnString += ", ";
            }
            node = node.getNext();

            counter += 1;
        }
        returnString += "]";
        return returnString;
    }

    /**
     * Gets the first value to use as a partition
     *
     * @return the first value in the list
     */
    public int getFirst()
    {
        if(this.getHead() == null)
        {
            throw new NullPointerException("List is empty");
        }

        return this.getHead().getVal();
    }

    /**
     * get the median of the first three values, handle exceptions
     *
     * @return the median of the first three values
     */
    public int getMedianFirstThree()
    {
        int first = -1;
        int second = -1;
        int third = -1;
        Node current = this.getHead();

        try
        {
            // get the first three values in the list
            first = current.getVal();
            current = current.getNext();
            second = current.getVal();
            current = current.getNext();
            third = current.getVal();
        }
        catch(NullPointerException npe)
        {
            // there are not three values in the list
            if(first == -1)
            {
                // the list is empty
                throw new RuntimeException("List is empty");
            }
            else
            {
                // the list has only 1-2 values, return first
                return first;
            }
        }

        // order the three nodes, then get the second (median) value
        LinkedList firstThree = new LinkedList();
        firstThree.insert(first);
        firstThree.insert(second);
        firstThree.insert(third);
        int median = firstThree.getHead().getNext().getVal();

        // special edge case to avoid infinite loop
        if(firstThree.getHead().getVal() ==
                firstThree.getHead().getNext().getVal())
        {
            return third;
        }

        return median;
    }

    /**
     * Puts the head of the list at the tail
     * helpful for avoiding loops in partitioning
     */
    public void putHeadAtTail()
    {
        Node head = this.getHead();
        try
        {
            Node second = head.getNext();
            this.setHead(second);
        }
        catch(NullPointerException npe)
        {
            // There was not a second node, function fails, do nothing
        }
        try
        {
            // place head at the end of the list, maintain list length
            this.append(head.getVal());
            this.length -= 1;
        }
        catch(NullPointerException npe)
        {
            // there was not a head, list is null, do nothing
        }
    }

    /**
     * Checks if the list is sorted
     *
     * @return true if the list is sorted, else false
     */
    public boolean isSorted()
    {
        boolean isSorted = true;
        Node node = this.getHead();

        if(this.head == null)
        {
            // list is empty, but is technically sorted
            return true;
        }

        while(node.getNext() != null)
        {
            if(node.getNext().getVal() < node.getVal())
            {
                // next value is less than parent, list is not sorted
                isSorted = false;
            }
            node = node.getNext();
        }
        return isSorted;
    }

    /**
     * Check if the list is entirely duplicates
     *
     * @return if the list is all duplicates
     */
    public boolean isAllDuplicate()
    {
        Node head = this.getHead();
        Node current = head;
        try
        {
            while(true)
            {
                if(head.getVal() != current.getVal())
                {
                    // list is not all duplicates
                    return false;
                }
                current = current.getNext();
            }
        }
        catch(NullPointerException npe)
        {
            // end of list, do nothing
        }

        // if we reach this point the list is all duplicates
        return true;
    }

    /**
     * Increments the length of the linked list by one
     */
    public void incLength()
    {
        this.length += 1;
    }

    /**
     * Gets the head of the linked list
     *
     * @return the head of the linked list
     */
    public Node getHead()
    {
        return this.head;
    }

    /**
     * Sets the head of the linked list
     *
     * @param head the head of the list
     */
    public void setHead(Node head)
    {
        this.head = head;
    }

    /**
     * Gets the length of the linked list
     *
     * @return the length of the linked list
     */
    public int getLength()
    {
        return this.length;
    }

    /**
     * Sets the length of the linked list
     *
     * @param length the head of the list
     */
    public void setLength(int length)
    {
        this.length = length;
    }
}
