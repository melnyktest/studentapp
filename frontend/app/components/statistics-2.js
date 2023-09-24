import Component from '@glimmer/component';
import { action } from '@ember/object';
import { tracked } from '@glimmer/tracking';

export default class Statistics2Component extends Component {
    @tracked courseGradesPerQuarter;

    constructor() {
        super(...arguments);
        this.getCourseGradesPerQuarter('mathmatics');
    }

    @action
    async updateCourse(e) {
        console.log(e.target.value);
        await this.getCourseGradesPerQuarter(e.target.value);
    }

    @action
    async getCourseGradesPerQuarter(course) {
        const response = await fetch(
            `http://localhost:8080/statistics/courseperquarter/${course}`,
            {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            },
        );

        const data = await response.json();
        this.courseGradesPerQuarter = data.data;
    }
}
