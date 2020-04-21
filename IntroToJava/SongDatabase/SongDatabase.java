 /**
  * This class creates the GUI application interface
  *
  * @author Brian Loughran
  */

 import javafx.application.*;
 import javafx.collections.FXCollections;
 import javafx.collections.ObservableList;
 import javafx.event.ActionEvent;
 import javafx.event.EventHandler;
 import javafx.scene.control.*;
 import javafx.scene.layout.GridPane;
 import javafx.scene.layout.HBox;
 import javafx.stage.Stage;
 import javafx.scene.*;
 import javafx.geometry.Insets;
 import javafx.geometry.Pos;
 import java.io.*;
 import java.util.*;
 import static java.lang.System.exit;

 public class SongDatabase extends Application
{
    private ArrayList<Song> Songs  = new ArrayList<Song>();
    // hidden variable to distinguish between adding an editing a song
    private String mode = "";
    private String databaseFilePath;

    // Title controls
    private Label titleLabel = new Label("Title: ");
    private ComboBox titleField = new ComboBox();

    // Item code controls
    private Label itemCodeLabel = new Label("Item Code: ");
    private TextField itemCodeField = new TextField();

    // Description controls
    private Label descriptionLabel = new Label("Description: ");
    private TextField descriptionField = new TextField();

    // Artist controls
    private Label artistLabel = new Label("Artist: ");
    private TextField artistField = new TextField();

    // Album controls
    private Label albumLabel = new Label("Album: ");
    private TextField albumField = new TextField();

    // Price controls
    private Label priceLabel = new Label("Price: ");
    private TextField priceField = new TextField();

    // Button controls
    private Button addButton = new Button("Add");
    private Button editButton = new Button("Edit");
    private Button deleteButton = new Button("Delete");
    private Button acceptButton = new Button("Accept");
    private Button cancelButton = new Button("Cancel");
    private Button exitButton = new Button("Exit");

    // error bar controls
    private Label errorBar = new Label("");


    public void start(Stage myStage)
    {
        databaseFilePath = getParameters().getUnnamed().get(0);
        Songs = readDB(databaseFilePath);

        if (Songs.isEmpty())
        {
            // initialize fields for empty song database
            createNewSongFile(databaseFilePath);
            editButton.setDisable(true);
            deleteButton.setDisable(true);
            acceptButton.setDisable(true);
            cancelButton.setDisable(true);
        }
        else
            {
            // initialize fields for non-empty song database
            setTitleOptions(getSongTitles(this.Songs));
            titleField.setValue(Songs.get(0).getTitle());
            itemCodeField.setText(Songs.get(0).getItemCode());
            descriptionField.setText(Songs.get(0).getDescription());
            artistField.setText(Songs.get(0).getArtist());
            albumField.setText(Songs.get(0).getAlbum());
            priceField.setText(Songs.get(0).getPriceString());
            acceptButton.setDisable(true);
            cancelButton.setDisable(true);
        }

        myStage.setTitle("Song Database");
        GridPane rootNode = new GridPane();
        Scene myScene = new Scene(rootNode, 500, 375);
        rootNode.setHgap(5);
        rootNode.setVgap(10);
        rootNode.setPadding(new Insets(20));

        // title formatting and handlers
        titleField.setVisibleRowCount(5);
        titleField.setPrefWidth(350);
        rootNode.add(titleLabel, 0, 0);
        rootNode.add(titleField, 1, 0);

        titleField.setOnAction(new TitleComboHandler());

        // item code formatting and handlers
        itemCodeField.setPrefWidth(50);
        itemCodeField.setEditable(false);
        rootNode.add(itemCodeLabel, 0, 1);
        rootNode.add(itemCodeField, 1, 1);

        // description formatting and handlers
        descriptionField.setPrefWidth(350);
        descriptionField.setEditable(false);
        rootNode.add(descriptionLabel, 0, 2);
        rootNode.add(descriptionField, 1, 2);

        // artist formatting and handlers
        artistField.setPrefWidth(350);
        artistField.setEditable(false);
        rootNode.add(artistLabel, 0, 3);
        rootNode.add(artistField, 1, 3);

        // album formatting and handlers
        albumField.setPrefWidth(350);
        albumField.setEditable(false);
        rootNode.add(albumLabel, 0, 4);
        rootNode.add(albumField, 1, 4);

        // title formatting and handlers
        priceField.setPrefWidth(50);
        priceField.setEditable(false);
        rootNode.add(priceLabel, 0, 5);
        rootNode.add(priceField, 1, 5);

        // button controls and handlers
        HBox buttons = new HBox(10);
        addButton.setPrefWidth(75);
        editButton.setPrefWidth(75);
        deleteButton.setPrefWidth(75);
        acceptButton.setPrefWidth(75);
        cancelButton.setPrefWidth(75);
        buttons.getChildren().addAll(addButton, editButton, deleteButton,
                acceptButton, cancelButton);
        buttons.setAlignment(Pos.CENTER);
        rootNode.add(buttons, 0, 6, 2, 1);

        addButton.setOnAction(new AddButtonHandler());
        editButton.setOnAction(new EditButtonHandler());
        deleteButton.setOnAction(new DeleteButtonHandler());
        acceptButton.setOnAction(new AcceptButtonHandler());
        cancelButton.setOnAction(new CancelButtonHandler());
        exitButton.setOnAction(new ExitButtonHandler());

        // exit button controls and handlers
        HBox exit = new HBox(10);
        exit.getChildren().add(exitButton);
        exitButton.setPrefWidth(50);
        exit.setAlignment(Pos.CENTER);
        rootNode.add(exit, 0, 7, 2, 1);

        // error bar controls and handlers
        rootNode.add(errorBar, 0, 8, 2, 1);

        // show the scene
        myStage.setScene(myScene);
        myStage.show();
    }

    /**
     * This class handles when a Title Bar event occurs
     *
     * @author Brian Loughran
     */
    class TitleComboHandler implements EventHandler<ActionEvent>
    {
        public void handle(ActionEvent e)
        {
            for(int i = 0; i < Songs.size(); i++)
            {
                if (Songs.get(i).getTitle().equals(titleField.getValue()))
                {
                    itemCodeField.setText(Songs.get(i).getItemCode());
                    descriptionField.setText(Songs.get(i).getDescription());
                    artistField.setText(Songs.get(i).getArtist());
                    albumField.setText(Songs.get(i).getAlbum());
                    priceField.setText(Songs.get(i).getPriceString());
                }
            }
        }
    }

    /**
     * This class handles when an Add Button event occurs
     *
     * @author Brian Loughran
     */
    class AddButtonHandler implements EventHandler<ActionEvent>
    {
        public void handle(ActionEvent e)
        {
            titleField.setEditable(true);
            titleField.setDisable(false);
            itemCodeField.setEditable(true);
            itemCodeField.setDisable(false);
            descriptionField.setEditable(true);
            artistField.setEditable(true);
            albumField.setEditable(true);
            priceField.setEditable(true);
            addButton.setDisable(true);
            editButton.setDisable(true);
            deleteButton.setDisable(true);
            acceptButton.setDisable(false);
            cancelButton.setDisable(false);
            mode = "ADD";

            titleField.setValue("");
            itemCodeField.setText("");
            descriptionField.setText("");
            artistField.setText("");
            albumField.setText("");
            priceField.setText("");
        }
    }

    /**
     * This class handles when an Edit Button event occurs
     *
     * @author Brian Loughran
     */
    class EditButtonHandler implements EventHandler<ActionEvent>
    {
        public void handle(ActionEvent e)
        {
            titleField.setEditable(false);
            titleField.setDisable(true);
            itemCodeField.setEditable(false);
            itemCodeField.setDisable(true);
            descriptionField.setEditable(true);
            artistField.setEditable(true);
            albumField.setEditable(true);
            priceField.setEditable(true);
            addButton.setDisable(true);
            editButton.setDisable(true);
            deleteButton.setDisable(true);
            acceptButton.setDisable(false);
            cancelButton.setDisable(false);
            mode = "EDIT";
        }
    }

    /**
     * This class handles when a Delete Button event occurs
     *
     * @author Brian Loughran
     */
    class DeleteButtonHandler implements EventHandler<ActionEvent>
    {
        public void handle(ActionEvent e)
        {
            for(int i = 0; i < Songs.size(); i++)
            {
                if(Songs.get(i).getTitle().equals(titleField.getValue()))
                {
                    deleteSong(Songs, Songs.get(i));
                }
            }

            try
            {
                titleField.setValue(Songs.get(0).getTitle());
                itemCodeField.setText((Songs.get(0).getItemCode()));
                descriptionField.setText((Songs.get(0).getDescription()));
                artistField.setText((Songs.get(0).getArtist()));
                albumField.setText((Songs.get(0).getAlbum()));
                priceField.setText((Songs.get(0).getPriceString()));
            }
            catch(IndexOutOfBoundsException indexException)
            {
                // clear fields if there are no songs left in the database
                titleField.setValue("");
                itemCodeField.setText("");
                descriptionField.setText("");
                artistField.setText("");
                albumField.setText("");
                priceField.setText("");
                editButton.setDisable(true);
                deleteButton.setDisable(true);
            }
            setTitleOptions(getSongTitles(Songs));
        }
    }

    /**
     * This class handles when a Cancel Button event occurs
     *
     * @author Brian Loughran
     */
    class CancelButtonHandler implements EventHandler<ActionEvent>
    {
        public void handle(ActionEvent e)
        {
            boolean songsEmpty = false;
            try
            {
                if (mode.equals("EDIT"))
                {
                    for (int i = 0; i < Songs.size(); i++)
                    {
                        if (Songs.get(i).getTitle().equals(titleField.getValue()))
                        {
                            // update fields for edited song
                            descriptionField.setText(Songs.get(i).getDescription());
                            artistField.setText(Songs.get(i).getArtist());
                            albumField.setText(Songs.get(i).getAlbum());
                            priceField.setText(Songs.get(i).getPriceString());
                        }
                    }
                }
                else if (mode == "ADD")
                {
                    // show fields for first song
                    titleField.setValue(Songs.get(0).getTitle());
                    itemCodeField.setText(Songs.get(0).getItemCode());
                    descriptionField.setText(Songs.get(0).getDescription());
                    albumField.setText(Songs.get(0).getAlbum());
                    artistField.setText(Songs.get(0).getArtist());
                    priceField.setText(Songs.get(0).getPriceString());
                }
            }
            catch(IndexOutOfBoundsException indexException)
            {
                // clear fields if no songs left in database
                titleField.setValue("");
                itemCodeField.setText("");
                descriptionField.setText("");
                artistField.setText("");
                albumField.setText("");
                priceField.setText("");

                songsEmpty = true;
            }

            titleField.setEditable(false);
            titleField.setDisable(false);
            itemCodeField.setEditable(false);
            itemCodeField.setDisable(false);
            descriptionField.setEditable(false);
            artistField.setEditable(false);
            albumField.setEditable(false);
            priceField.setEditable(false);
            addButton.setDisable(false);
            editButton.setDisable(false);
            deleteButton.setDisable(false);
            acceptButton.setDisable(true);
            cancelButton.setDisable(true);

            if(songsEmpty)
            {
                editButton.setDisable(true);
                deleteButton.setDisable(true);
            }
            else
            {
                editButton.setDisable(false);
                deleteButton.setDisable(false);
            }

            errorBar.setText("");
            mode = "";
        }
    }

    /**
     * This class handles when an Accept Button event occurs
     *
     * @author Brian Loughran
     */
    class AcceptButtonHandler implements EventHandler<ActionEvent>
    {
        public void handle(ActionEvent e)
        {
            if(mode.equals("EDIT"))
            {
                // get data from fields
                String title = titleField.getValue().toString();
                String itemCode = itemCodeField.getText();
                String description = descriptionField.getText();
                String artist = artistField.getText();
                String album = albumField.getText();

                try
                {
                    double price = Double.valueOf(priceField.getText());
                    // create new song object
                    Song editedSong = new Song(title, itemCode, description,
                            artist, album, price);

                    for (int i = 0; i < Songs.size(); i++)
                    {
                        if (Songs.get(i).getTitle().equals(
                                editedSong.getTitle()))
                        {
                            // update fields with song data
                            Songs.set(i, editedSong);
                            descriptionField.setText(Songs.get(i).getDescription());
                            artistField.setText(Songs.get(i).getArtist());
                            albumField.setText(Songs.get(i).getAlbum());
                            priceField.setText(Songs.get(i).getPriceString());
                        }
                    }
                }

                // catch if price is non-numeric
                catch(NumberFormatException numException)
                {
                    errorBar.setText("Price must be numeric");
                    return;
                }

                // catch if song input data is invalid
                catch(Exception otherException)
                {
                    errorBar.setText(otherException.getMessage());
                    return;
                }
            }
            else if(mode.equals("ADD"))
            {
                // collect info from fields
                String title = titleField.getValue().toString();
                String itemCode = itemCodeField.getText();
                String description = descriptionField.getText();
                String artist = artistField.getText();
                String album = albumField.getText();

                try
                {
                    double price = Double.valueOf(priceField.getText());
                    // create new song object
                    Song addedSong = new Song(title, itemCode, description,
                            artist, album, price);

                    Songs.add(addedSong);
                    setTitleOptions(getSongTitles(Songs));

                    // update gui fields with added song data
                    titleField.setValue(addedSong.getTitle());
                    itemCodeField.setText(addedSong.getItemCode());
                    descriptionField.setText(addedSong.getDescription());
                    artistField.setText(addedSong.getArtist());
                    albumField.setText(addedSong.getAlbum());
                    priceField.setText(addedSong.getPriceString());

                    checkUniqueItemCode(Songs, addedSong);

                }

                // catch if price is non-numeric
                catch(NumberFormatException numException)
                {
                    errorBar.setText("Price must be numeric");
                    return;
                }

                // catch if input data invalid
                catch(Exception otherException)
                {
                    errorBar.setText(otherException.getMessage());
                    return;
                }
            }

            titleField.setEditable(false);
            titleField.setDisable(false);
            itemCodeField.setEditable(false);
            itemCodeField.setDisable(false);
            descriptionField.setEditable(false);
            artistField.setEditable(false);
            albumField.setEditable(false);
            priceField.setEditable(false);
            addButton.setDisable(false);
            editButton.setDisable(false);
            deleteButton.setDisable(false);
            acceptButton.setDisable(true);
            cancelButton.setDisable(true);

            errorBar.setText("");
            mode = "";
        }
    }

    /**
     * This class handles when an Exit Button event occurs
     *
     * @author Brian Loughran
     */
    class ExitButtonHandler implements EventHandler<ActionEvent>
    {
        public void handle(ActionEvent e)
        {
            // save and exit
            writeDB(databaseFilePath, Songs);
            exit(0);
        }
    }

    /**
     * Read song db file and return songs
     *
     * @param filePath the file path of the database
     *
     * @return an ArrayList of songs
     */
    public static ArrayList<Song> readDB(String filePath)
    {
        // empty line
        String line = "";

        // initialize new Songs ArrayList
        ArrayList<Song> Songs = new ArrayList<Song>();

        try
        {
            BufferedReader br = new BufferedReader(new FileReader(filePath));

            // go until no more lines in file
            while ((line = br.readLine()) != null) {

                // use comma as separator
                String[] commaSeperatedSong = line.split(",");

                String title = commaSeperatedSong[0].trim();
                String itemCode = commaSeperatedSong[1].trim();
                String description = commaSeperatedSong[2].trim();
                String artist = commaSeperatedSong[3].trim();
                String album = commaSeperatedSong[4].trim();
                double price = Double.parseDouble(commaSeperatedSong[5].trim());

                // create new song
                Song song = new Song(title, itemCode, description, artist,
                        album, price);

                Songs.add(song);
            }
        }
        catch (FileNotFoundException notFound)
        {
            // do nothing...
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }

        return Songs;
    }

    /**
     * Add a song to song list
     *
     * @param filePath the file path of the database
     * @param Songs an ArrayList of songs
     */
    public static void writeDB(String filePath, ArrayList<Song> Songs)
    {
        try
        {
            // initialize output file
            File outFile = new File(filePath);
            FileOutputStream outputStream = new FileOutputStream(outFile);
            BufferedWriter writer = new BufferedWriter(
                    new OutputStreamWriter(outputStream));

            for (int i = 0; i < Songs.size(); i++)
            {
                // write new comma seperated value line to file
                writer.write(Songs.get(i).getCsvLine());
                writer.newLine();
            }
            writer.close();
        }
        catch (Exception FileNotFoundException)
        {
            System.out.println("File not found");
        }
    }

    /**
     * Delete a song from the song list
     *
     * @param songs the list of songs
     * @param song the song to delete
     *
     * @return an ArrayList of songs
     */
    public static ArrayList<Song> deleteSong(ArrayList<Song> songs, Song song)
    {
        for(int i = 0; i < songs.size(); i++)
        {
            if(songs.get(i) == song)
            {
                songs.remove(i);
            }
        }
        return songs;
    }

    /**
     * Create a new song file if needed
     *
     * @param newFilePath the file path of the song file
     */
    public static void createNewSongFile(String newFilePath)
    {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Would you like to create a new song file? ");
        System.out.println("(1 for yes, 0 for no): ");
        int selection = scanner.nextInt();

        switch(selection)
        {
            case 0:
            {
                // exit the program
                exit(0);
            }
            case 1:
            {
                try
                {
                    FileOutputStream newFile = new FileOutputStream(
                            newFilePath);
                }
                catch(FileNotFoundException nf)
                {
                    System.out.println("Did not find created file");
                    return;
                }
                break;
            }
            default:
            {
                System.out.println("Enter 1 for yes, 0 for no: ");
            }
        }
    }

    /**
     *
     * @param songs a list of songs
     *
     * @return the list of song titles
     */
    public static ObservableList<String> getSongTitles(ArrayList<Song> songs)
    {
        // observable list is the required object type to change combo box
        ObservableList<String> songTitles = FXCollections.observableArrayList();
        for(int i = 0; i < songs.size(); i++)
        {
            songTitles.add(songs.get(i).getTitle());
        }
        return songTitles;
    }

    /**
     * Set the tile options of the titleField combobox
     *
     * @param titles an observable list of titles
     *               (usually supplied by getSongTitles)
     */
    public void setTitleOptions(ObservableList<String> titles)
    {
        this.titleField.setItems(titles);
    }

    /**
     * Thrown an exception if a song is added with a non-unique item code
     *
     * @param songs an ArrayList of Song containing the database
     * @param song the added Song object
     */
    public static void checkUniqueItemCode(ArrayList<Song> songs, Song song)
    {
        for(int i = 0; i < songs.size(); i++)
        {
            if(song.getItemCode().equals(songs.get(i).getItemCode()))
            {
                throw new RuntimeException("Item code must be unique");
            }
        }
    }
}
