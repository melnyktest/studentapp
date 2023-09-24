import Component from '@glimmer/component';
import { action } from '@ember/object';
import { tracked } from '@glimmer/tracking';

export default class StatisticsComponent extends Component {
    @tracked students;
    @tracked studentAvgGradePerQuarter;

    constructor() {
        super(...arguments);
        this.getStudents().then((data) => {
            this.students = data;
            this.getStudentAvgGradePerQuarter(data[0].id);
        });
    }

    @action
    async getStudents() {
        const response = await fetch(`http://localhost:8080/student`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        const data = await response.json();
        return data.data;
    }

    @action
    async getStudentAvgGradePerQuarter(student_id) {
        const response = await fetch(
            `http://localhost:8080/statistics/studentperquarter/${student_id}`,
            {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            },
        );

        const data = await response.json();
        this.studentAvgGradePerQuarter = data.data;
    }

    @action
    async updateStudentId(e) {
        await this.getStudentAvgGradePerQuarter(e.target.value);
    }
}
