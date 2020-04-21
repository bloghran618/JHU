 /*
  * This is the main class which prints out all possible paths
  */

 import java.io.*;
 import java.util.Arrays;

 public class walkGraphs
{
    public static void main(String args[])
    {
        // Special Features:
        // Section to show input that was not recognized by the program
        // Do not assume adj list only contains 1's and 0's
        // Recognized graphs are identified in number order
        // Print the number of paths from one node to the next
        // Print the number of valid graphs
        // Print the binary and linked implementations of the graph

        String inputFile = args[0];
        String outputFile = args[1];

        clearOutput(outputFile);

        writeToOutputFile(outputFile, "Unrecognized input:\n");

        Graph[] graphs = readGraphs(inputFile, outputFile);

        int numGraphs = 0;
        while(graphs[numGraphs] != null)
        {
            numGraphs++; // count the number of recognized graphs
        }

        writeToOutputFile(outputFile, "\nRecognized Input:\n");
        writeToOutputFile(outputFile, numGraphs +
                " graphs recognized\n\n");
        for(int k = 0; k < numGraphs; k++)
        {
            writeToOutputFile(outputFile, "Graph #" + (k+1) + "\n");
            writeToOutputFile(outputFile, graphs[k].getGraphString());
            writeToOutputFile(outputFile, "\n");
        }

        PathsString paths = new PathsString();

        for(int k = 0; k < numGraphs; k++) // loop over each graph
        {
            writeToOutputFile(outputFile, "\nPaths on Graph: " +
                    (k+1) + "\n");

            int numNodes = graphs[k].getNumNodes();

            // loop over each starting point
            for(int start = 1; start <= numNodes; start++)
            {
                // loop over each destination
                for(int dest = 1; dest <= numNodes; dest++)
                {
                    // initialize hasVisited to all false
                    boolean[] hasVisited = new boolean[numNodes];
                    Arrays.fill(hasVisited, false);

                    // initialize current path to start node
                    Integer[] currentPath = new Integer[numNodes+1];
                    Arrays.fill(currentPath, null);
                    currentPath[0] = start;

                    // clear any current paths
                    paths.clear();

                    // recursively get string of all paths
                    getAllPaths(start, start, dest, hasVisited, currentPath,
                            graphs[k], paths);

                    writeToOutputFile(outputFile,
                            "There are " + paths.getNumPaths() +
                                    " paths from " + start + " to " + dest +
                                    " on graph #" + (k+1) + ":\n");
                    writeToOutputFile(outputFile, paths.getPaths());
                    writeToOutputFile(outputFile, "\n\n");
                }
            }
        }
    }

    /**
     * Reads the text file into a list of Graph objects
     *
     * @param inputFile the path of the input file
     * @param outputFile the name of the output file
     *
     * @return a list of valid graph objects
     */
    public static Graph[] readGraphs(String inputFile, String outputFile)
    {
        // can read in a max of 1000 graphs
        Graph[] graphs = new Graph[1000];

        String line;

        // keep track of if we are loading graph size or node adj list
        boolean isAdjList = false;

        // number of nodes in the current graph
        int numNodes = 0;
        int currentNode = 0;
        Graph currentGraph = new Graph(1);
        int currentGraphNumber = 0;
        String inlines = "";

        try {
            BufferedReader br = new BufferedReader(new FileReader(inputFile));

            while ((line = br.readLine()) != null)
            {
                try
                {
                    inlines += line.replace("\n", "") + "\n";

                    if(isAdjList)
                    {
                        String[] spaceDelimitedLine = line.split(" ");
                        int[] intLine = new int[spaceDelimitedLine.length];


                        for(int j = 0; j < spaceDelimitedLine.length; j++)
                        {
                            intLine[j] = Integer.parseInt(
                                    spaceDelimitedLine[j]);
                        }


                        if(intLine.length != numNodes)
                        {
                            throw new RuntimeException("Adjacency list " +
                                    "improper length");
                        }
                        else
                        {
                            for(int l = 0; l < spaceDelimitedLine.length; l++)
                            {
                            }
                            currentGraph.addAdjListAtNode(currentNode,
                                    intLine);
                            currentNode++;
                        }
                    }
                    else
                    {
                        numNodes = Integer.parseInt(line);
                        currentGraph = new Graph(numNodes);
                        isAdjList = true;
                    }

                    if(currentNode >= numNodes)
                    {
                        // Graph has been fully read
                        graphs[currentGraphNumber] = currentGraph;
                        currentGraphNumber++;
                        isAdjList = false;
                        currentNode = 0;
                        inlines = "";
                    }
                }
                catch (Exception e)
                {
                    // if exception wait until start of next good graph
                    isAdjList = false;
                    currentNode = 0;

                    // write any lines to output that were previously good
                    writeToOutputFile(outputFile, inlines);

                    inlines = "";
                }
            }
        }
        catch (FileNotFoundException notFound)
        {
            System.out.println("File not found");
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
        return graphs;
    }

    /**
     * Write a string to output
     *
     * @param file the path of the output file
     * @param outputString the line to write to the output file
     */
    public static void writeToOutputFile(String file, String outputString)
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

    /**
     * Converts an integer list to a path string
     *
     * @param currentPath the path to convert to string
     *
     * @return the string of the path
     */
    public static String getCurrentPath(Integer[] currentPath)
    {
        int length = currentPath.length;
        String returnString = "[";

        for(int k = 0; k < length; k++)
        {
            if(currentPath[k] != null)
            {
                returnString += currentPath[k] + ", ";
            }
        }
        if(!returnString.equals("["))
        {
            // crop off the last ", " in the list if not empty
            returnString = returnString.substring(0,
                    returnString.length() - 2);
        }
        returnString += "]";

        return returnString;
    }

    /**
     * Recursive function to get all paths for a particular graph
     *
     * @param start the starting node
     * @param current the current node
     * @param dest the destination node
     * @param hasVisited a boolean list designating which nodes were visited
     * @param currentPath an integer list designating the current path
     * @param graph the Graph object we are searching
     * @param paths a PathsString object keeping track of valid paths
     */
    public static void getAllPaths(Integer start, Integer current,
                                     Integer dest, boolean[] hasVisited,
                                     Integer[] currentPath, Graph graph,
                                     PathsString paths)
    {
        hasVisited[current - 1] = true;

        if(current == dest && current != start)
        {
            paths.append(getCurrentPath(currentPath));
        }

        int[] adjList = graph.getNodes()[current-1].toList();

        // loop over each neighbor in adj list
        for(int neighbor: adjList)
        {
            if(neighbor == dest && neighbor == start) // include loops to start
            {
                int j = 0;
                while(currentPath[j] != null)
                {
                    j++; // end of while loop j will be first non-null val
                }
                currentPath[j] = neighbor; // add current node to path
                paths.append(getCurrentPath(currentPath));
                currentPath[j] = null; // cleanup
            }

            // if we have not visited neighbor yet
            if(!hasVisited[neighbor-1])
            {
                int j = 0;
                while(currentPath[j] != null)
                {
                    j++; // end of while loop j will be first non-null val
                }
                currentPath[j] = neighbor; // add neighbor to current path

                getAllPaths(start, neighbor, dest, hasVisited, currentPath,
                        graph, paths);

                currentPath[j] = null; // cleanup
            }
        }
        hasVisited[current-1] = false; // cleanup
    }
}