/*
 * This class is a translator between morse code and english
 */

import java.util.Scanner;
import java.util.regex.Pattern;

public class MorseCode
{
    public static void main(String[] args)
    {
        char[] english = { 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8',
                '9', '0', ',', '.', '?', ' ' };

        String[] morse = { ".-", "-...", "-.-.", "-..", ".", "..-.", "--.",
                "....", "..", ".---", "-.-", ".-..", "--", "-.", "---",
                ".---.", "--.-", ".-.", "...", "-", "..-", "...-", ".--",
                "-..-", "-.--", "--..", ".----", "..---", "...--", "....-",
                ".....", "-....", "--...", "---..", "----.", "-----", "--..--",
                ".-.-.-", "..--..", "|" };

        Scanner keyboard = new Scanner(System.in);

        // Get user input language
        System.out.println("This is a translator between " +
                "English and Morse Code!");
        System.out.println("Will your input be in english or morse?");
        System.out.print("Enter english for english, or morse for morse: ");
        String input_language = keyboard.nextLine().toLowerCase();

        // Initialize output
        String str = "";

        switch(input_language)
        {
            case "english":

                // Get the line to translate
                System.out.print("Enter english string: ");
                String english_input = keyboard.nextLine().toLowerCase();

                char[] chars = english_input.toCharArray();

                for (int i = 0; i < chars.length; i++)
                {
                    for (int j = 0; j < english.length; j++)
                    {

                        if (english[j] == chars[i])
                        {
                            // append found letter to output string
                            str = str + morse[j] + " ";
                        }
                    }
                }
                break;

            case "morse":

                // get the line to translate
                System.out.print("Enter morse code string: ");
                String morse_input = keyboard.nextLine().toLowerCase();

                String[] morse_list = morse_input.split(Pattern.quote(" "));

                for (int i = 0; i < morse_list.length; i++)
                {
                    for (int j = 0; j < morse.length; j++)
                    {

                        if (morse[j].equals(morse_list[i]))
                        {
                            // append found morse character to output string
                            str = str + english[j];
                        }
                    }
                }
                break;

            default:
                System.out.println("There was an error with your input");
                break;

        }

        System.out.println(str);
    }
}
