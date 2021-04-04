<template>
  <div id="app">
    <k-progress 
      status="success" 
      type="line"
      :line-height="14"
      :percent=firstPercentage >
    </k-progress>
    <k-progress 
      status="success" 
      type="line"
      :line-height="14"
      :percent=secondPercentage>
    </k-progress>
    <k-progress 
      status="success" 
      type="line"
      :line-height="14"
      :percent=thirdPercentage>
    </k-progress>
    <k-progress 
      status="success" 
      type="line"
      :line-height="14"
      :percent=fourthPercentage>
    </k-progress>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  
  data () {
    return {
      firstPercentage: null,
      secondPercentage: null,
      thirdPercentage: null,
      fourthPercentage: null
    }
  },

  mounted () {
  
    const
        AreaType = "overview",
        AreaName = "United Kingdom";

    const
        filters = [
            `areaType=${ AreaType }`,
            `areaName=${ AreaName }`
        ],
        structure = {
            date: "date",
            name: "areaName",
            code: "areaCode",
            // cases: {
            //     new: "newCasesByPublishDate",
            //     cumulative: "cumCasesByPublishDate"
            // },
            // deaths: {
            //     new: "newDeathsByDeathDate",
            //     cumulative: "cumDeathsByDeathDate"
            // }
            "vaccines": {
              "first_dose": {
                  "daily": "newPeopleVaccinatedFirstDoseByPublishDate",
                  "cumulative": "cumPeopleVaccinatedFirstDoseByPublishDate",
              },
              "second_dose": {
                  "daily": "newPeopleVaccinatedSecondDoseByPublishDate",
                  "cumulative": "cumPeopleVaccinatedSecondDoseByPublishDate",
              },
            }
        };

    const
        apiParams = {
            filters: filters.join(";"),
            structure: JSON.stringify(structure),
        };

    const endpoint = 'https://api.coronavirus.data.gov.uk/v1/data';

    axios.get(endpoint, { 
        params: apiParams,
        timeout: 10000 
    }).then((data, status, statusText) => {
      console.log(status)
      console.log(statusText)
      if (status >= 400) {
        this.info = 0;
      }
      else {
        const ukPop = 68098857
        const ukAdultPop = 68098857 - 12700000
        const today = data["data"]["data"][0];
        const firstDose = today["vaccines"]["first_dose"]["cumulative"]
        const secondDose = today["vaccines"]["second_dose"]["cumulative"]
        this.firstPercentage = (firstDose / ukPop) * 100
        this.secondPercentage = ((firstDose + secondDose) / (ukPop * 2)) * 100
        this.thirdPercentage = (firstDose / ukAdultPop) * 100
        this.fourthPercentage = ((firstDose + secondDose) / (ukAdultPop * 2)) * 100
      }
    });

  }
}

</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
