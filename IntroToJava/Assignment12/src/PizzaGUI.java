/*
 * This class creates and handles a simple pizza price calculation GUI
 */

import javafx.application.*;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.geometry.Pos;
import javafx.scene.*;
import javafx.scene.control.*;
import javafx.stage.*;
import javafx.scene.layout.*;
import javafx.geometry.Insets;
import java.util.Scanner;

import javax.swing.*;

public class PizzaGUI extends Application
{
    // Size controls
    private RadioButton small = new RadioButton("Small");
    private RadioButton medium = new RadioButton("Medium");
    private RadioButton large = new RadioButton("Large");

    // Toppings Controls
    private CheckBox plain = new CheckBox("Plain");
    private CheckBox sausage = new CheckBox("Sausage");
    private CheckBox mushroom = new CheckBox("Mushroom");
    private CheckBox pepperoni = new CheckBox("Pepperoni");

    // Price Controls
    private Label priceLabel = new Label("Price: ");
    private TextField priceField = new TextField();

//    public void main(String args[])
//    {
//        System.out.println(args[0]);
//    }

    public void start(Stage myStage)
    {
        Scanner scanner = new Scanner(System.in);
        int input = scanner.nextInt();

        myStage.setTitle("Radio Button Programming Excercise");
        GridPane rootNode = new GridPane();
        Scene myScene = new Scene(rootNode, 250, 200);
        rootNode.setHgap(5);
        rootNode.setVgap(30);
        rootNode.setPadding(new Insets(30));
        rootNode.setAlignment(Pos.CENTER);

        // Pizza size formatting and handlers
        small.setSelected(true);

        small.setOnAction(new smallRadioHandler());
        medium.setOnAction(new mediumRadioHandler());
        large.setOnAction(new largeRadioHandler());

        ToggleGroup smallMediumLarge = new ToggleGroup();
        small.setToggleGroup(smallMediumLarge);
        medium.setToggleGroup(smallMediumLarge);
        large.setToggleGroup(smallMediumLarge);

        HBox size = new HBox(8);
        size.getChildren().addAll(small, medium, large);

        rootNode.add(size, 0, 0);

        // Toppings formatting and handlers
        plain.setSelected(true);

        plain.setOnAction(new plainCheckHandler());
        sausage.setOnAction(new sausageCheckHandler());
        mushroom.setOnAction(new mushroomCheckHandler());
        pepperoni.setOnAction(new pepperoniCheckHandler());

        HBox toppingsTop = new HBox(8);
        toppingsTop.getChildren().addAll(plain, sausage);
        HBox toppingsBottom = new HBox(8);
        toppingsBottom.getChildren().addAll(mushroom, pepperoni);
        VBox toppings = new VBox(8);
        toppings.getChildren().addAll(toppingsTop, toppingsBottom);

        rootNode.add(toppings, 0, 1);

        // Price formatting and handlers
        priceField.setText("$6.00");

        priceField.setEditable(false);
        priceField.setPrefWidth(75);

        HBox price = new HBox(8);
        price.getChildren().addAll(priceLabel, priceField);

        rootNode.add(price, 0, 2);

        myStage.setScene(myScene);
        myStage.show();
    }

    class smallRadioHandler implements EventHandler<ActionEvent>
    {
        public void handle(ActionEvent e)
        {
            double price = 5.00;
                if(!plain.isSelected())
                {
                    if(sausage.isSelected())
                    {
                        price += 0.50;
                    }
                    if(mushroom.isSelected())
                    {
                        price += 0.50;
                    }
                    if(pepperoni.isSelected())
                    {
                        price += 0.50;
                    }
                }
                priceField.setText(String.format("$%.2f", price));
        }
    }

    class mediumRadioHandler implements EventHandler<ActionEvent>
    {
        public void handle(ActionEvent e)
        {
            double price = 8.00;
                if(!plain.isSelected())
                {
                    if(sausage.isSelected())
                    {
                        price += 1.00;
                    }
                    if(mushroom.isSelected())
                    {
                        price += 1.00;
                    }
                    if(pepperoni.isSelected())
                    {
                        price += 1.00;
                    }
                }
                priceField.setText(String.format("$%.2f", price));
        }
    }

    class largeRadioHandler implements EventHandler<ActionEvent>
    {
        public void handle(ActionEvent e)
        {
            double price = 12.00;
                if(!plain.isSelected())
                {
                    if(sausage.isSelected())
                    {
                        price += 1.50;
                    }
                    if(mushroom.isSelected())
                    {
                        price += 1.50;
                    }
                    if(pepperoni.isSelected())
                    {
                        price += 1.50;
                    }
                }
                priceField.setText(String.format("$%.2f", price));
        }
    }

    class plainCheckHandler implements EventHandler<ActionEvent>
    {
        public void handle(ActionEvent e)
        {
            if(plain.isSelected())
                {
                    sausage.setSelected(false);
                    mushroom.setSelected(false);
                    pepperoni.setSelected(false);
                }

                double price = 0.00;

                if(small.isSelected())
                {
                    price += 5.00;

                    if(sausage.isSelected())
                    {
                        price += 0.50;
                    }
                    if(mushroom.isSelected())
                    {
                        price += 0.50;
                    }
                    if(pepperoni.isSelected())
                    {
                        price += 0.50;
                    }

                }
                else if(medium.isSelected())
                {
                    price += 8.00;

                    if(sausage.isSelected())
                    {
                        price += 1.00;
                    }
                    if(mushroom.isSelected())
                    {
                        price += 1.00;
                    }
                    if(pepperoni.isSelected())
                    {
                        price += 1.00;
                    }
                }
                else
                {
                    price += 12.00;

                    if(sausage.isSelected())
                    {
                        price += 1.50;
                    }
                    if(mushroom.isSelected())
                    {
                        price += 1.50;
                    }
                    if(pepperoni.isSelected())
                    {
                        price += 1.50;
                    }
                }
                priceField.setText(String.format("$%.2f", price));
        }
    }

    class sausageCheckHandler implements EventHandler<ActionEvent>
    {
        public void handle(ActionEvent e)
        {
            if(sausage.isSelected())
                {
                    plain.setSelected(false);
                }

                double price = 0.00;

                if(small.isSelected())
                {
                    price += 5.00;

                    if(sausage.isSelected())
                    {
                        price += 0.50;
                    }
                    if(mushroom.isSelected())
                    {
                        price += 0.50;
                    }
                    if(pepperoni.isSelected())
                    {
                        price += 0.50;
                    }

                }
                else if(medium.isSelected())
                {
                    price += 8.00;

                    if(sausage.isSelected())
                    {
                        price += 1.00;
                    }
                    if(mushroom.isSelected())
                    {
                        price += 1.00;
                    }
                    if(pepperoni.isSelected())
                    {
                        price += 1.00;
                    }
                }
                else
                {
                    price += 12.00;

                    if(sausage.isSelected())
                    {
                        price += 1.50;
                    }
                    if(mushroom.isSelected())
                    {
                        price += 1.50;
                    }
                    if(pepperoni.isSelected())
                    {
                        price += 1.50;
                    }
                }
                priceField.setText(String.format("$%.2f", price));
        }
    }

    class mushroomCheckHandler implements EventHandler<ActionEvent>
    {
        public void handle(ActionEvent e)
        {
            if(mushroom.isSelected())
                {
                    plain.setSelected(false);
                }

                double price = 0.00;

                if(small.isSelected())
                {
                    price += 5.00;

                    if(sausage.isSelected())
                    {
                        price += 0.50;
                    }
                    if(mushroom.isSelected())
                    {
                        price += 0.50;
                    }
                    if(pepperoni.isSelected())
                    {
                        price += 0.50;
                    }

                }
                else if(medium.isSelected())
                {
                    price += 8.00;

                    if(sausage.isSelected())
                    {
                        price += 1.00;
                    }
                    if(mushroom.isSelected())
                    {
                        price += 1.00;
                    }
                    if(pepperoni.isSelected())
                    {
                        price += 1.00;
                    }
                }
                else
                {
                    price += 12.00;

                    if(sausage.isSelected())
                    {
                        price += 1.50;
                    }
                    if(mushroom.isSelected())
                    {
                        price += 1.50;
                    }
                    if(pepperoni.isSelected())
                    {
                        price += 1.50;
                    }
                }
                priceField.setText(String.format("$%.2f", price));
        }
    }

    class pepperoniCheckHandler implements EventHandler<ActionEvent>
    {
        public void handle(ActionEvent e)
        {
            if(pepperoni.isSelected())
                {
                    plain.setSelected(false);
                }

                double price = 0.00;

                if(small.isSelected())
                {
                    price += 5.00;

                    if(sausage.isSelected())
                    {
                        price += 0.50;
                    }
                    if(mushroom.isSelected())
                    {
                        price += 0.50;
                    }
                    if(pepperoni.isSelected())
                    {
                        price += 0.50;
                    }

                }
                else if(medium.isSelected())
                {
                    price += 8.00;

                    if(sausage.isSelected())
                    {
                        price += 1.00;
                    }
                    if(mushroom.isSelected())
                    {
                        price += 1.00;
                    }
                    if(pepperoni.isSelected())
                    {
                        price += 1.00;
                    }
                }
                else
                {
                    price += 12.00;

                    if(sausage.isSelected())
                    {
                        price += 1.50;
                    }
                    if(mushroom.isSelected())
                    {
                        price += 1.50;
                    }
                    if(pepperoni.isSelected())
                    {
                        price += 1.50;
                    }
                }
                priceField.setText(String.format("$%.2f", price));
        }
    }
}
