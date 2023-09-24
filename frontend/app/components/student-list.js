import Component from '@glimmer/component';
import { action } from '@ember/object';
import { tracked } from '@glimmer/tracking';

export default class StudentListComponent extends Component {
    @tracked students;
    @tracked name;
    @tracked birth_date;
    @tracked class_name;
    @tracked year = '2022';
    @tracked quarter = 'Q1';
    @tracked mathematics = '5';
    @tracked computer = '5';
    @tracked literature = '5';
    @tracked isNotFetchAble = false;
    @tracked fetchCount = 5;
    @tracked fetchStartId = 1;

    constructor() {
        super(...arguments);
        this.fetchStudent(this.fetchStartId, this.fetchStartId + this.fetchCount - 1);
    }

    @action
    async fetchStudent(fetchSt, fetchEn) {
        const response = await fetch(`http://localhost:8080/student/${fetchSt}/${fetchEn}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        const data = await response.json();
        this.students = data.data;
        if (this.students.length < this.fetchCount) this.isNotFetchAble = true;
        else this.isNotFetchAble = false;
    }
    @action
    updateName(e) {
        this.name = e.target.value;
    }
    @action
    updateBirthDate(e) {
        this.birth_date = e.target.value;
    }
    @action
    updateClassName(e) {
        this.class_name = e.target.value;
    }
    @action
    updateEnrollmentYear(e) {
        this.year = e.target.value;
    }
    @action
    updateQuarter(e) {
        this.quarter = e.target.value;
    }
    @action
    updateMathematicsGrade(e) {
        this.mathmatics = e.target.value;
    }
    @action
    updateComputerGrade(e) {
        this.computer = e.target.value;
    }
    @action
    updateLiteratureGrade(e) {
        this.literature = e.target.value;
    }
    @action
    async updateFetchCount(e) {
        this.fetchCount = parseInt(e.target.value);
        console.log(e.target.value)
        console.log(this.fetchStartId)
        await this.fetchStudent(this.fetchStartId, this.fetchStartId + this.fetchCount - 1)
    }
    @action
    async prevPage() {
        if (this.fetchStartId >= this.fetchCount) {
            this.fetchStartId = this.fetchStartId - this.fetchCount
        } else {
            this.fetchStartId = 1;
        }
        await this.fetchStudent(this.fetchStartId, this.fetchCount + this.fetchStartId - 1)
        this.isNotFetchAble = false;
        console.log(this.fetchSt)
    }
    @action
    async nextPage() {
        this.fetchStartId = this.fetchStartId + this.fetchCount
        await this.fetchStudent(this.fetchStartId, this.fetchStartId + this.fetchCount - 1)
        if (this.students.length < this.fetchCount) this.isNotFetchAble = true;
        else this.isNotFetchAble = false;

        console.log("fetchable: ", this.isNotFetchAble)
    }
    @action
    async addGrade() {
        event.preventDefault();
        const data = {
            name: this.name,
            birth_date: this.birth_date,
            class_name: this.class_name,
            year: this.year,
            quarter: this.quarter,
            mathmatics: this.mathmatics,
            computer: this.computer,
            literature: this.literature,
        };
        const response = await fetch('http://localhost:8080/student', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        location.reload();

        if (response.status == 200) {
            alert('Grade added successfully!');
        } else {
            alert('Server Error');
        }
    }
    @action
    async deleteUser(student_id) {
        console.log(student_id)
        const response = await fetch(
            `http://localhost:8080/student/delete/${student_id}`,
            {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            },
        );

       
    }

    @action
    async editUser(student) {
        console.log(student);
        this.name = student.name;
        this.birth_date = student.birth_date;
        this.class_name = student.class_name;
        this.year = 2020;
        this.maths = 5;
        this.computer = 5;
        this.literature = 5;
        this.quarter = 'Choose Quarter';
    }
}
