/*
 * This class is the main class of the sorting lab
 */

import java.io.*;

public class sortMain
{
    public static void main(String args[])
    {
        // ENHANCEMENTS
        // 1. Program will not crash if line is not int
        // 2. Program will tell you what input is unrecognized/ignored
        // 3. Deal with duplicates
        // 4. Experiment with files of size 20K

        String inputFile = args[0];
        String outputFile = args[1];

        runAndTimeSorts(inputFile, outputFile);
    }

    /**
     * Do a merge sort and print the results of the different sorts
     * This will output the results of 5 sorts:
     *   - Quicksort with first item as partition and size 1-2 stopping case
     *   - Quicksort with first item as partition and size 50 stopping case
     *   - Quicksort with first item as partition and size 100 stopping case
     *   - Quicksort with median first three partition and size 1-2 stopping case
     *   - Natural merge sort
     *
     *  The method will also time each sort and put the results to the output
     *
     * @param inputFile the input file to read
     * @param outputFile the output file to read
     */
    public static void runAndTimeSorts(String inputFile, String outputFile)
    {
        clearOutput(outputFile);

        // read input
        writeToOutput("Unrecognized Input: \n", outputFile);
        LinkedList linkedList1 = readInput(inputFile, outputFile);

        writeToOutput("\nRecognized Input: \n", outputFile);
        writeToOutput(linkedList1.toString() + "\n\n", outputFile);

        // create multiple copies of the original linked list (sorting destroys)
        LinkedList linkedList2 = new LinkedList(linkedList1);
        LinkedList linkedList3 = new LinkedList(linkedList1);
        LinkedList linkedList4 = new LinkedList(linkedList1);
        LinkedList linkedList5 = new LinkedList(linkedList1);

        // run quicksort case 1
        long quick1_2StartTime = System.nanoTime();
        LinkedList quick1_2SortedList = quickSort1_2(linkedList1);
        long quick1_2EndTime = System.nanoTime();
        long duration = (quick1_2EndTime - quick1_2StartTime); //divide by 1000000 to get milliseconds.

        writeToOutput("\n\nQuick Sort with a stopping case of " +
                "1 and 2 took " + duration + " nanoseconds", outputFile);

        // run quicksort case 2
        long quick50StartTime = System.nanoTime();
        LinkedList quick50SortedList = quickSort50(linkedList2);
        long quick50EndTime = System.nanoTime();
        duration = (quick50EndTime - quick50StartTime); //divide by 1000000 to get milliseconds.

        writeToOutput("\n\nQuick Sort with a stopping case of " +
                "50 took " + duration + " nanoseconds", outputFile);

        // run quicksort case 3
        long quick100StartTime = System.nanoTime();
        LinkedList quick100SortedList = quickSort100(linkedList3);
        long quick100EndTime = System.nanoTime();
        duration = (quick100EndTime - quick100StartTime); //divide by 1000000 to get milliseconds.

        writeToOutput("\n\nQuick Sort with a stopping case of " +
                "100 took " + duration + " nanoseconds", outputFile);

        // run quicksort case 4
        long quickMed3StartTime = System.nanoTime();
        LinkedList quickMed3SortedList = quickSortMedian(linkedList4);
        long quickMed3EndTime = System.nanoTime();
        duration = (quickMed3EndTime - quickMed3StartTime); //divide by 1000000 to get milliseconds.

        writeToOutput("\n\nQuick Sort using the median of the" +
                " first three took " + duration + " nanoseconds", outputFile);

        // run natural merge sort
        long naturalMergeStartTime = System.nanoTime();
        LinkedList naturalMergeSortedList = naturalMergeSort(linkedList5);
        long naturalMergeEndTime = System.nanoTime();
        duration = (naturalMergeEndTime - naturalMergeStartTime); //divide by 1000000 to get milliseconds.

        writeToOutput("\n\nNatural merge took " + duration +
                " nanoseconds", outputFile);

        writeToOutput("\n\nQuicksort stopping case of 1 and 2 output:" +
                " \n", outputFile);
        writeToOutput(quick1_2SortedList.toString(), outputFile);

        writeToOutput("\n\nQuicksort stopping case of 50 output:" +
                " \n", outputFile);
        writeToOutput(quick50SortedList.toString(), outputFile);

        writeToOutput("\n\nQuicksort stopping case of 100 output:" +
            " \n", outputFile);
        writeToOutput(quick100SortedList.toString(), outputFile);

        writeToOutput("\n\nQuicksort median of three output:" +
                " \n", outputFile);
        writeToOutput(quickMed3SortedList.toString(), outputFile);

        writeToOutput("\n\nNatural Merge output:" +
                " \n", outputFile);
        writeToOutput(naturalMergeSortedList.toString(), outputFile);
    }

    /**
     * A quicksort algorithm with a stopping case of 2
     *
     * @param linked the linked list to sort
     *
     * @return the sorted linked list
     */
    public static LinkedList quickSort1_2(LinkedList linked)
    {
        int length = linked.getLength();

        // array 2x size of linked list will be big enough to store partitinos
        LinkedList[] linkedPartitionedCurrent = new LinkedList[length * 2];
        linkedPartitionedCurrent[0] = linked;
        LinkedList[] linkedPartitionedNext = new LinkedList[length * 2];

        int maxSize = length;
        int index = 0;

        // initializer so we do not have to declare in loop
        LinkedList[] overUnderPartitions;

        // iterate until max size of partition < 2
        while(maxSize > 2)
        {
            // check each partitioned list
            for(LinkedList part: linkedPartitionedCurrent)
            {
                try
                {
                    // only partition if above stopping case
                    if (part.getLength() > 2)
                    {
                        overUnderPartitions = partition(part, part.getFirst());
                        linkedPartitionedNext[index] = overUnderPartitions[0];
                        index += 1;
                        linkedPartitionedNext[index] = overUnderPartitions[1];
                        index += 1;
                    }
                    else if(part.getLength() != 0)
                    {
                        linkedPartitionedNext[index] = part;
                        index += 1;
                    }
                    else
                    {
                        // empty, do not store value, do nothing
                    }
                }
                catch(NullPointerException npe)
                {
                    // list is null, do nothing, do not store it
                }
            }

            // resetting max size
            maxSize = 0;
            for(LinkedList part: linkedPartitionedNext)
            {
                try
                {
                    if (part.getLength() > maxSize)
                    {
                        maxSize = part.getLength();
                    }
                }
                catch(NullPointerException npe)
                {
                    // do nothing
                }
            }

            // managing linked partition versions
            linkedPartitionedCurrent = linkedPartitionedNext;
            linkedPartitionedNext = new LinkedList[length];
            index = 0;
        }

        // sort partitioned lists
        LinkedList sorted = new LinkedList();
        for(LinkedList part: linkedPartitionedCurrent)
        {
            try
            {
                sorted.appendList(insertionSort(part));
            }
            catch(NullPointerException npe)
            {
                // do nothing
            }
        }

        return sorted;
    }

    /**
     * A quicksort algorithm with a stopping case of 50
     *
     * @param linked the linked list to sort
     *
     * @return the sorted linked list
     */
    public static LinkedList quickSort50(LinkedList linked)
    {
        int length = linked.getLength();

        // array 2x size of linked list will be big enough to store partitinos
        LinkedList[] linkedPartitionedCurrent = new LinkedList[length * 2];
        linkedPartitionedCurrent[0] = linked;
        LinkedList[] linkedPartitionedNext = new LinkedList[length * 2];

        int maxSize = length;
        int index = 0;

        // initializer so we do not have to declare in loop
        LinkedList[] overUnderPartitions;

        // iterate until max size of partition < 2
        while(maxSize > 50)
        {
            // check each partitioned list
            for(LinkedList part: linkedPartitionedCurrent)
            {
                try
                {
                    // only partition if above stopping case
                    if (part.getLength() > 50)
                    {
                        overUnderPartitions = partition(part, part.getFirst());
                        linkedPartitionedNext[index] = overUnderPartitions[0];
                        index += 1;
                        linkedPartitionedNext[index] = overUnderPartitions[1];
                        index += 1;
                    }
                    else if(part.getLength() != 0)
                    {
                        linkedPartitionedNext[index] = part;
                        index += 1;
                    }
                    else
                    {
                        // forget empty list, do nothing
                    }
                }
                catch(NullPointerException npe)
                {
                    // list is null, do nothing, do not store it
                }
            }

            // resetting max size
            maxSize = 0;
            for(LinkedList part: linkedPartitionedNext)
            {
                try
                {
                    if (part.getLength() > maxSize)
                    {
                        maxSize = part.getLength();
                    }
                }
                catch(NullPointerException npe)
                {
                    // do nothing
                }
            }

            // managing linked partition versions
            linkedPartitionedCurrent = linkedPartitionedNext;
            linkedPartitionedNext = new LinkedList[length];
            index = 0;
        }

        // sort partitioned lists
        LinkedList sorted = new LinkedList();
        for(LinkedList part: linkedPartitionedCurrent)
        {
            try
            {
                sorted.appendList(insertionSort(part));
            }
            catch(NullPointerException npe)
            {
                // do nothing
            }
        }

        return sorted;
    }

    /**
     * A quicksort algorithm with a stopping case of 100
     *
     * @param linked the linked list to sort
     *
     * @return the sorted linked list
     */
    public static LinkedList quickSort100(LinkedList linked)
    {
        int length = linked.getLength();

        // array 2x size of linked list will be big enough to store partitinos
        LinkedList[] linkedPartitionedCurrent = new LinkedList[length * 2];
        linkedPartitionedCurrent[0] = linked;
        LinkedList[] linkedPartitionedNext = new LinkedList[length * 2];

        int maxSize = length;
        int index = 0;

        // initializer so we do not have to declare in loop
        LinkedList[] overUnderPartitions;

        // iterate until max size of partition < 2
        while(maxSize > 100)
        {
            // check each partitioned list
            for(LinkedList part: linkedPartitionedCurrent)
            {
                try
                {
                    // only partition if above stopping case
                    if (part.getLength() > 100)
                    {
                        overUnderPartitions = partition(part, part.getFirst());
                        linkedPartitionedNext[index] = overUnderPartitions[0];
                        index += 1;
                        linkedPartitionedNext[index] = overUnderPartitions[1];
                        index += 1;
                    }
                    else if(part.getLength() != 0)
                    {
                        linkedPartitionedNext[index] = part;
                        index += 1;
                    }
                    else
                    {
                        // forget empty list, do nothing
                    }
                }
                catch(NullPointerException npe)
                {
                    // list is null, do nothing, do not store it
                }
            }

            // resetting max size
            maxSize = 0;
            for(LinkedList part: linkedPartitionedNext)
            {
                try
                {
                    if (part.getLength() > maxSize)
                    {
                        maxSize = part.getLength();
                    }
                } catch (NullPointerException npe)
                {
                    // do nothing
                }
            }

            // managing linked partition versions
            linkedPartitionedCurrent = linkedPartitionedNext;
            linkedPartitionedNext = new LinkedList[length];
            index = 0;
        }

        // sort partitioned lists
        LinkedList sorted = new LinkedList();
        for(LinkedList part: linkedPartitionedCurrent)
        {
            try
            {
                sorted.appendList(insertionSort(part));
            }
            catch(NullPointerException npe)
            {
                // do nothing
            }
        }

        return sorted;
    }

    /**
     * A quicksort algorithm with a stopping case of 2, using the median value
     * to partition the list
     *
     * @param linked the linked list to sort
     *
     * @return the sorted linked list
     */
    public static LinkedList quickSortMedian(LinkedList linked)
    {
        int length = linked.getLength();

        // array 2x size of linked list will be big enough to store partitinos
        LinkedList[] linkedPartitionedCurrent = new LinkedList[length * 2];
        linkedPartitionedCurrent[0] = linked;
        LinkedList[] linkedPartitionedNext = new LinkedList[length * 2];

        int maxSize = length;
        int index = 0;

        // initializer so we do not have to declare in loop
        LinkedList[] overUnderPartitions;

        // iterate until max size of partition < 2
        while(maxSize > 2)
        {
            // check each partitioned list
            for(LinkedList part: linkedPartitionedCurrent)
            {
                try
                {
                    // only partition if above stopping case
                    if (part.getLength() > 2)
                    {
                        int median = part.getMedianFirstThree();
                        overUnderPartitions = partition(part, median);
                        linkedPartitionedNext[index] = overUnderPartitions[0];
                        index += 1;
                        linkedPartitionedNext[index] = overUnderPartitions[1];
                        index += 1;
                    }
                    else if(part.getLength() != 0)
                    {
                        linkedPartitionedNext[index] = part;
                        index += 1;
                    }
                    else
                    {
                        // empty, do nothing, do not store
                    }
                }
                catch(NullPointerException npe)
                {
                    // list is null, do nothing, do not store it
                }
            }

            // resetting max size
            maxSize = 0;
            for(LinkedList part: linkedPartitionedNext)
            {
                try
                {
                    if (part.getLength() > maxSize)
                    {
                        maxSize = part.getLength();
                    }
                }
                catch(NullPointerException npe)
                {
                    // do nothing
                }
            }

            // managing linked partition versions
            linkedPartitionedCurrent = linkedPartitionedNext;
            linkedPartitionedNext = new LinkedList[length];
            index = 0;
        }

        LinkedList sorted = new LinkedList();
        // sort partitioned lists
        for(LinkedList part: linkedPartitionedCurrent)
        {
            try
            {
                sorted.appendList(insertionSort(part));
            }
            catch(NullPointerException npe)
            {
                // do nothing
            }
        }

        return sorted;
    }

    /**
     * Partitions a linked list
     *
     * @param linked the linked list to partition
     * @param partition the integer to partition around
     *
     * @return the partition to the left and the right of the pivot
     */
    public static LinkedList[] partition(LinkedList linked, int partition)
    {
        LinkedList linkedUnder = new LinkedList();
        LinkedList linkedOver = new LinkedList();

        // linked list is duplicate of itself, split in even halves
        if(linked.isAllDuplicate())
        {
            try
            {
                while(true)
                {
                    // fill each duplicate linked list evenly by managing length
                    if(linkedUnder.getLength() < linkedOver.getLength())
                    {
                        linkedUnder.append(linked.getHead().getVal());
                    }
                    else
                    {
                        linkedOver.append(linked.getHead().getVal());
                    }
                    linked.setHead(linked.getHead().getNext());
                }
            }
            catch(NullPointerException npe)
            {
                // end of list, do nothing
            }
        }
        // linked list contains unique values, separate by pivot
        else
        {
            try
            {
                while (true)
                {
                    if (linked.getHead().getVal() < partition)
                    {
                        linkedUnder.append(linked.getHead().getVal());
                    }
                    else
                    {
                        linkedOver.append(linked.getHead().getVal());
                    }
                    linked.setHead(linked.getHead().getNext());
                }
            }
            catch (NullPointerException npe)
            {
                // end of the list, do nothing
            }

            // shuffle values so we dont get stuck in infinite loop
            linkedOver.putHeadAtTail();
            linkedUnder.putHeadAtTail();
        }

        // return two linked lists
        LinkedList[] linkedPartition = new LinkedList[2];
        linkedPartition[0] = linkedUnder;
        linkedPartition[1] = linkedOver;

        return linkedPartition;
    }

    /**
     * an algorithm to do a natural merge sort on a linked implementation
     *
     * @param linkedList the linked list to sort
     *
     * @return the sorted linked list
     */
    public static LinkedList naturalMergeSort(LinkedList linkedList)
    {
        // maintain length of the linked list
        int length = linkedList.getLength();

        LinkedList sorted = new LinkedList();
        LinkedList firstLinked = new LinkedList();
        LinkedList secondLinked = new LinkedList();

        do
        {
            // keep track of value before current
            int lastVal = -1;
            int currentVal = linkedList.getHead().getVal();
            try
            {
                // loop until the end of the linked list
                while (true)
                {
                    firstLinked.setHead(null);
                    secondLinked.setHead(null);

                    // populate first list to merge
                    while (lastVal <= currentVal)
                    {
                        firstLinked.append(currentVal);
                        linkedList.setHead(linkedList.getHead().getNext());
                        lastVal = currentVal;
                        currentVal = linkedList.getHead().getVal();
                    }
                    lastVal = -1;
                    // populate second list to merge
                    while (lastVal <= currentVal)
                    {
                        secondLinked.append(currentVal);
                        linkedList.setHead(linkedList.getHead().getNext());
                        lastVal = currentVal;
                        currentVal = linkedList.getHead().getVal();
                    }

                    // merge first and second ordered lists and add to sorted
                    sorted.appendList(merge(firstLinked, secondLinked));

                    lastVal = -1;
                }
            }
            catch (NullPointerException npe)
            {
                // end of list, append everything still in memory before delete
                if (secondLinked != null)
                {
                    // merge two lists and append
                    sorted.appendList(merge(firstLinked, secondLinked));
                }
                else
                {
                    // append just one list
                    sorted.appendList(firstLinked);
                }

                // cleanup
                firstLinked.setHead(null);
                secondLinked.setHead(null);
            }

            if (!sorted.isSorted())
            {
                linkedList = sorted;
            }
        } while(!sorted.isSorted()); // do until list is sorted

        // maintain length
        sorted.setLength(length);

        return sorted;
    }

    /**
     * Merge two linked lists (assumes they are already sorted)
     *
     * @param linkedLista linked list to merge
     * @param linkedListb linked list to merge
     *
     * @return one merged linked list
     */
    public static LinkedList merge(LinkedList linkedLista,
                                       LinkedList linkedListb)
    {
        LinkedList sorted = new LinkedList();

        // if one list empty, return the other
        if(linkedLista.getHead() == null)
        {
            return linkedListb;
        }
        if(linkedListb.getHead() == null)
        {
            return linkedLista;
        }

        Node currentaNode = linkedLista.getHead();
        Node currentbNode = linkedListb.getHead();

        // compare values in each list and add lowest to sorted
        while(currentaNode != null && currentbNode != null)
        {
            if(currentaNode.getVal() <= currentbNode.getVal())
            {
                // top of a less than b, append a
                sorted.append(currentaNode.getVal());
                currentaNode = currentaNode.getNext();
            }
            else
            {
                // top of b less than a, append b
                sorted.append(currentbNode.getVal());
                currentbNode = currentbNode.getNext();
            }
        }

        // after one list is empty, put the end of the other list in sorted
        try
        {
            while(currentaNode != null || currentbNode != null)
            {
                if(currentaNode == null)
                {
                    // push the rest of list b
                    sorted.append(currentbNode.getVal());
                    currentbNode = currentbNode.getNext();
                }
                if(currentbNode == null)
                {
                    // push the rest of list a
                    sorted.append(currentaNode.getVal());
                    currentaNode = currentaNode.getNext();
                }
            }
        }
        catch(NullPointerException npe)
        {
            // do nothing
        }

        return sorted;
    }

    /**
     * An insertion sort algorithm using a linked implementation
     *
     * @param linkedList the linked list to sort
     *
     * @return the sorted linked list
     */
    public static LinkedList insertionSort(LinkedList linkedList)
    {
        LinkedList sorted = new LinkedList();
        Node current = linkedList.getHead();

        try
        {
            while(true) // loop until current == null
            {
                sorted.insert(current.getVal());
                current = current.getNext();
            }
        }
        catch(NullPointerException npe)
        {
            // do nothing
        }

        return sorted;
    }

    /**
     * Reads the text file into a LinkedList
     *
     * @param inputFile the path of the input file
     * @param outputFile the name of the output file
     *
     * @return a valid LinkedList
     */
    public static LinkedList readInput(String inputFile, String outputFile)
    {
        // initializers
        String line;
        int value;
        LinkedList linkedList = new LinkedList();

        try
        {
            BufferedReader br = new BufferedReader(new FileReader(inputFile));

            while ((line = br.readLine()) != null)
            {
                try
                {
                    value = Integer.parseInt(line);

                    // add value to linked list
                    linkedList.append(value);
                }
                catch(NumberFormatException nfe)
                {
                    // catch bad input, record it, and do not add to list
                    writeToOutput(line + "\n", outputFile);
                }
            }
        }
        catch (FileNotFoundException notFound)
        {
            System.out.println("File not found");
            // do nothing
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }

        return linkedList;
    }

    /**
     * Write a string to output
     *
     * @param outputString the line to write to the output file
     * @param file the path of the output file
     */
    public static void writeToOutput(String outputString, String file)
    {
        Writer output;
        try
        {
            // write the string to the end of the file
            output = new BufferedWriter(new FileWriter(file, true));
            output.append(outputString);
            output.close();
        }
        catch (Exception exception)
        {
            // do nothing
        }
    }

    /**
     * Clear text in the output file
     *
     * @param file the path of the output file
     */
    public static void clearOutput(String file)
    {
        try
        {
            PrintWriter pw = new PrintWriter(file);
            pw.close();
        }
        catch (FileNotFoundException fileNotFound)
        {
            // do nothing
        }
    }

}
