import Component from '@glimmer/component';
import { action } from '@ember/object';
import { tracked } from '@glimmer/tracking';

export default class Statistics3Component extends Component {
    @tracked quarters;
    @tracked quarterAvgGradeForCourses;

    constructor() {
        super(...arguments);
        this.getQuarters().then((data) => {
            this.quarters = data;
            console.log("data: ", data);
            this.getYearQuarterGeneralAvgGrade(this.quarters[0].id)
        })
    }

    @action
    async updateQuarter(e) {
        await this.getYearQuarterGeneralAvgGrade(e.target.value)
    }

    @action
    async getQuarters() {
        const response = await fetch(`http://localhost:8080/quarter`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        const data = await response.json()
        return data.data
    }
    @action
    async getYearQuarterGeneralAvgGrade(quarter_id) {
        const response = await fetch(`http://localhost:8080/statistics/quartergradeforcourses/${quarter_id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },  
        });

        const data = await response.json()
        this.quarterAvgGradeForCourses = data.data;
    }
}
