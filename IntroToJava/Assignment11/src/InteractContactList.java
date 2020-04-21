 /*
  * This class is used to interact with the contact list
  */

import java.io.*;
import java.util.*;

 public class InteractContactList
{
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);

        // sample input file attached Contacts.txt
        System.out.print("Enter contacts file path: ");
        String contactFilePath = input.nextLine();
        System.out.println();

        TreeMap<String, Contact> contacts = new TreeMap<String, Contact>();

        contacts = readFile(contactFilePath);

        int selection = 1;
        while(selection != 5)
        {
            switch (selection) {
                case 1: {
                    printMenu();
                    break;
                }

                case 2: {
                    contacts = addContact(contacts);
                    writeFile(contactFilePath, contacts);
                    break;
                }

                case 3:
                {
                    contacts = deleteContact(contacts);
                    writeFile(contactFilePath, contacts);
                    break;
                }
                case 4:
                {
                   printContacts(contacts);
                   break;
                }
                default:
                {
                    System.out.println("Please enter number 1-5\n");
                }
            }

            System.out.print("Enter Selection: ");
            selection = input.nextInt();
        }

        System.out.println("Exiting Session");
        writeFile(contactFilePath, contacts);
    }

    // show user available commands
    public static void printMenu()
    {
        System.out.println("1. Menu");
        System.out.println("2. Add Contact");
        System.out.println("3. Delete Contact");
        System.out.println("4. Display Contacts");
        System.out.println("5. Exit\n\n");

    }

    // add a contact to the list (maintain alphabetical order)
    public static TreeMap<String, Contact> addContact(
            TreeMap<String, Contact> contacts)
    {
        Scanner input = new Scanner(System.in);

        System.out.print("Enter First Name: ");
        String first = input.nextLine();
        System.out.print("Enter Last Name: ");
        String last = input.nextLine();
        System.out.print("Enter Company Name: ");
        String company = input.nextLine();
        System.out.print("Enter Phone Number: ");
        String phone = input.nextLine();
        System.out.print("Enter Email: ");
        String email = input.nextLine();

        System.out.println("\n");

        Contact contact = new Contact(first, last, company, phone, email);

        contacts.put(contact.getFirstLastKey(), contact);

        return contacts;
    }

    // remove a contact from the list by key
    public static TreeMap<String, Contact> deleteContact(TreeMap<String,
            Contact> contacts)
    {
        Scanner input = new Scanner(System.in);

        System.out.print("Enter the Last and First name " +
                "of the contact to delete: ");
        // Example: "Loughran Brian"
        String firstLastKey = input.nextLine();

        System.out.println("\n");

        if(contacts.containsKey(firstLastKey))
        {
            contacts.remove(firstLastKey);
            System.out.print(firstLastKey + " deleted");
        }
        else
        {
            System.out.println("Last First Key does not exist in contacts");
        }

        System.out.println("\n");

        return contacts;
    }

    public static void printContacts(TreeMap<String, Contact> contacts)
    {
        System.out.println("\n");

        for(Map.Entry<String, Contact> entry : contacts.entrySet())
        {
            System.out.println("First: " + entry.getValue().getFirst());
            System.out.println("Last: " + entry.getValue().getLast());
            System.out.println("Co: " + entry.getValue().getCompany());
            System.out.println("Phone: " + entry.getValue().getPhone());
            System.out.println("Email: " + entry.getValue().getEmail());

            System.out.println();
        }

        System.out.println("\n");
    }

    public static TreeMap<String, Contact> readFile(String contactFilePath)
    {
        TreeMap<String, Contact> contacts = new TreeMap<String, Contact>();

        try
        {
            // read file
            File dataFile = new File(contactFilePath);
            FileReader fileReader = new FileReader(dataFile);
            BufferedReader bufferedReader = new BufferedReader(fileReader);

            String line;
            while((line = bufferedReader.readLine()) != null)
            {
                // convert string index to proper field
                String first = line.substring(0, 10).trim();
                String last = line.substring(10, 25).trim();
                String company = line.substring(25, 50).trim();
                String phone = line.substring(50, 70).trim();
                String email = line.substring(70, 110).trim();

                Contact contact = new Contact(first, last, company, phone,
                        email);

                contacts.put(contact.getFirstLastKey(), contact);
            }
            fileReader.close();
        }
        catch(NullPointerException e)
        {
            System.out.println("Records var (args[2]) is too high");
        }
        catch(Exception e)
        {
            e.printStackTrace();
        }

        return contacts;
    }

    public static void writeFile(String filePath,
                                 TreeMap<String, Contact> contacts)
    {
        try
        {
            File outFile = new File(filePath);
            FileOutputStream outputStream = new FileOutputStream(outFile);
            BufferedWriter writer = new BufferedWriter(
                    new OutputStreamWriter(outputStream));

            for (Map.Entry<String, Contact> entry : contacts.entrySet())
            {
                Contact contact = entry.getValue();
                writer.write(contact.writeFileString());
                writer.newLine();
            }
            writer.close();
        }
        catch (Exception FileNotFoundException)
        {
            System.out.println("File not found");
        }
    }
}
