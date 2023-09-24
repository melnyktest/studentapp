    import Component from '@glimmer/component';
    import Ember from 'ember';
    import * as am5 from '@amcharts/amcharts5';
    import * as am5xy from '@amcharts/amcharts5/xy';

    export default Ember.Component.extend({
        init() {
            this._super(...arguments);
            this.set("preData", this.data);
            this.set("rootFlag", false);
        },
        didReceiveAttrs() {
            this._super(...arguments);
            if (this.data !== this.preData) {
                console.log("update")
                this.send("cleanup");
                this.send("createElement");
            }
        },
        actions: {
            createElement() {
                let root = am5.Root.new(document.getElementById("amchart"));
                this.root = root;
                var chart;
                chart = root.container.children.push(
                    am5xy.XYChart.new(root, {
                        panY: false,
                        layout: root.verticalLayout,
                    }),
                );
                this.chart = chart;
                let data = this.data || [];
                console.log("Amchart:", data)

                // Create Y-axis
                let yAxis = chart.yAxes.push(
                    am5xy.ValueAxis.new(root, {
                        renderer: am5xy.AxisRendererY.new(root, {}),
                        max: 10,
                        min: 0,
                    }),
                );

                // Create X-Axis
                let xAxis = chart.xAxes.push(
                    am5xy.CategoryAxis.new(root, {
                        renderer: am5xy.AxisRendererX.new(root, {}),
                        categoryField: 'category',
                        max: 10,
                        min: 0,
                    }),
                );
                xAxis.data.setAll(data);

                // Create series
                let series1 = chart.series.push(
                    am5xy.ColumnSeries.new(root, {
                        name: 'Series',
                        xAxis: xAxis,
                        yAxis: yAxis,
                        valueYField: 'value1',
                        categoryXField: 'category',
                    }),
                );
                series1.data.setAll(data);

                // Add legend
                let legend = chart.children.push(am5.Legend.new(root, {}));
                legend.data.setAll(chart.series.values);

                // Add cursor
                chart.set('cursor', am5xy.XYCursor.new(root, {}));
            },
            cleanup() {
                if (this.chart) {
                    this.chart.dispose();
                }
                if (this.root) {
                    this.root.dispose();
                }
            }
        }


    })
