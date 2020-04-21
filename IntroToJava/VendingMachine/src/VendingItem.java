/**
 * This class represents items that can be loaded into the vending machine
 *
 * @author Brian Loughran
 */

public class VendingItem
{
    private String item;
    private String item_package;
    private int cost; // item cost is denoted in pennies, e.g. %1.50 = 150
    private int quantity;
    /**
     * Initialize the VendingItem object
     *
     * @param item a String representing the item to consume
     * @param item_package a String representing the item container
     * @param cost an integer representing the cost of the item
     * @param quantity an integer representing the quantity of item loaded
     */
    public VendingItem(String item, String item_package, int cost, int quantity)
    {
        if (item != "")
        {
            this.item = item;
        }
        else
        {
            throw new RuntimeException("Item cannot be left blank");
        }

        if (item_package != "")
        {
            this.item_package = item_package;
        }
        else
        {
            throw new RuntimeException("Item package cannot be left blank");
        }

        if (cost >= 0)
        {
            this.cost = cost;
        }
        else
        {
            throw new RuntimeException("Item cost cannot be negative");
        }

        if (quantity >= 0)
        {
            this.quantity = quantity;
        }
        else
        {
            throw new RuntimeException("Quantity cannot be negative");
        }
    }

    /**
     * Increment the quantity of an item down by one
     */
    public void buyOne()
    {
        if (this.quantity > 0)
        {
            this.quantity -= 1;
        }
        else
        {
            System.out.println(this.item + " is sold out!");
        }
    }

    /**
     * Set item variable
     *
     * @param item the item to consume
     */
    public void setItem(String item)
    {
        this.item = item;
    }

    /**
     * Get item variable
     *
     * @return the item
     */
    public String getItem()
    {
        return this.item;
    }

    /**
     * Set item_package variable
     *
     * @param item_package the package containing the item
     */
    public void setItem_package(String item_package)
    {
        this.item_package = item_package;
    }

    /**
     * Get item_package variable
     *
     * @return the item package
     */
    public String getItem_package()
    {
        return this.item_package;
    }

    /**
     * Set cost variable
     *
     * @param cost the cost of the item in pennies
     */
    public void setCost(int cost)
    {
        this.cost = cost;
    }

    /**
     * Get cost variable
     *
     * @return the cost
     */
    public int getCost()
    {
        return this.cost;
    }

    /**
     * Set quantity variable
     *
     * @param quantity the quantity of an item
     */
    public void setQuantity(int quantity)
    {
        this.quantity = quantity;
    }

    /**
     * Get quantity variable
     *
     * @return the quantity of an item
     */
    public int getQuantity()
    {
        return this.quantity;
    }


}
