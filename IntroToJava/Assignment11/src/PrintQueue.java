/*
 * This class controls adding and displaying the print queue
 */

import java.util.LinkedList;
import java.util.Scanner;
import java.util.List;

public class PrintQueue
{
    public static void main(String[] args)
    {
        Scanner input = new Scanner(System.in);

        // create linked list for print queue
        List<Job> queue = new LinkedList<Job>();

        // job numbers are assigned sequentially starting at 0
        int jobSerial = 0;

        int selection = 0;
        while (selection != 2)
        {
            printMenu();

            System.out.print("Enter Selection: ");
            selection = input.nextInt();

            switch(selection)
            {
                case 1:
                {
                    queue = addJob(queue, jobSerial);
                    jobSerial++;
                    break;
                }

                case 2:
                {
                    printJobs(queue);
                    break;
                }

                default:
                {
                    System.out.println("Please enter a number 1-2\n");
                }
            }
        }
    }

    // add a job to the queue
    public static List<Job> addJob(List<Job> queue, int jobSerial)
    {
        Job job = new Job(jobSerial);
        queue.add(job);

        System.out.println();

        return queue;
    }

    // format and display jobs in the queue
    public static void printJobs(List<Job> queue)
    {
        System.out.println("Job #     Print Time");
        System.out.println("-------   ----------");

        int i = 0;
        while(i < queue.size())
        {
            queue.get(i).formatJob();
            i++;
        }
    }

    // show the user the available commands
    public static void printMenu()
    {
        System.out.println("1. Add job");
        System.out.println("2. Exit and display jobs\n");
    }
}


