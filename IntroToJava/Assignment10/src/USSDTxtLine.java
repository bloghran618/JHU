 /*
  * This class represents one line in USSD13.txt
  */

 import java.io.Serializable;

 public class USSDTxtLine implements Serializable
{
    protected String stateCode;
    protected String districtID;
    protected String districtName;
    protected int totalPopulation;
    protected int relevantPopulation;
    protected int povertyChildren;
    protected String tag;

    public USSDTxtLine(String stateCode, String districtID, String districtName,
                       int totalPopulation, int relevantPopulation,
                       int povertyChildren, String tag)
    {
        if (stateCode != "" && districtID != "" && districtName != "" &&
                totalPopulation >= 0 && relevantPopulation >= 0 &&
                povertyChildren >= 0 && tag != "")
        {
            this.stateCode = stateCode;
            this.districtID = districtID;
            this.districtName = districtName;
            this.totalPopulation = totalPopulation;
            this.relevantPopulation = relevantPopulation;
            this.povertyChildren = povertyChildren;
            this.tag = tag;
        }
        else
        {
            throw new RuntimeException("Invalid input to USSDTextLine Class");
        }
    }

    public String getStateCode()
    {
        return this.stateCode;
    }

    public void setStateCode(String stateCode)
    {
        this.stateCode = stateCode;
    }

    public String getDistrictID()
    {
        return this.districtID;
    }

    public void setDistrictID(String districtID)
    {
        this.districtID = districtID;
    }

    public String getDistrictName()
    {
        return this.districtName;
    }

    public void setDistrictName(String districtName)
    {
        this.districtName = districtName;
    }

    public int getTotalPopulation()
    {
        return this.totalPopulation;
    }

    public void setTotalPopulation(int totalPopulation)
    {
        this.totalPopulation = totalPopulation;
    }

    public int getRelevantPopulation()
    {
        return this.relevantPopulation;
    }

    public void setRelevantPopulation(int relevantPopulation)
    {
        this.relevantPopulation = relevantPopulation;
    }

    public int getPovertyChildren()
    {
        return this.povertyChildren;
    }

    public void setPovertyChildren(int povertyChildren)
    {
        this.povertyChildren = povertyChildren;
    }

    public String getTag()
    {
        return this.tag;
    }

    public void setTag(String tag)
    {
        this.tag = tag;
    }
}
