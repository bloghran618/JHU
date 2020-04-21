 /*
  * This class represents a summarized verison of USSDTxtLine from census data
  */

 import java.io.Serializable;

 public class SummaryLine extends USSDTxtLine implements Serializable
{
    private float percentPoverty;

    public SummaryLine(String stateCode, String districtID,
                            String districtName, int totalPopulation,
                            int relevantPopulation, int povertyChildren,
                            String tag)
    {
        super(stateCode, districtID, districtName, totalPopulation,
                relevantPopulation, povertyChildren, tag);

        percentPoverty = (float)povertyChildren / relevantPopulation * 100;
    }

    public void printReportHeader()
    {
        System.out.println("State   Population  Child Population " +
                "Child Poverty Population  % Child Poverty");
        System.out.println("-----   ----------  ---------------- " +
                "------------------------  ---------------");
    }

    public void printReportLine()
    {
        System.out.format("%5s   %10d  %16d %24d  %15.2f\n",
                this.getStateCode(), this.getTotalPopulation(),
                this.getRelevantPopulation(), this.getPovertyChildren(),
                this.getPercentPoverty());
    }

    // this function is used to add children to a district to existing summary
    public void addDistrict(USSDTxtLine district)
    {
        int totalPopulation = this.getTotalPopulation() +
                district.getTotalPopulation();
        int relevantPopulation = this.getRelevantPopulation() +
                district.getRelevantPopulation();
        int povertyChildren = this.getPovertyChildren() +
                district.getPovertyChildren();

        this.setTotalPopulation(totalPopulation);
        this.setRelevantPopulation(relevantPopulation);
        this.setPovertyChildren(povertyChildren);
        this.percentPoverty = (float)this.getPovertyChildren() /
            this.getRelevantPopulation() * 100;
    }

    public float getPercentPoverty()
    {
        return this.percentPoverty;
    }

    public void setPercentPoverty(float percentPoverty)
    {
        this.percentPoverty = percentPoverty;
    }

}
