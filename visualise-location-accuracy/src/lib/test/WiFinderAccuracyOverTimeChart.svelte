<script lang="ts">
	import { Chart as C, type ChartOptions } from 'chart.js';
	import { Chart } from 'chart.js/auto';
	import annotation from 'chartjs-plugin-annotation';
	import dayjs from 'dayjs';
	import { wiFinderLocationData } from '$lib/locations/locationsData';
	import { currentPlayingTimeSeconds, startTimeForTestPreview } from './playbackTimes';
	import { averageWifinderAccuracy, wiFinderLocationAccuracy } from './wifinderAccuracy';

	C.register(annotation);

	let data = $derived({
		labels: $wiFinderLocationData.map(({ timestamp }) =>
			dayjs(timestamp).diff($startTimeForTestPreview, 'seconds')
		),
		datasets: [
			{
				data: $wiFinderLocationAccuracy,
				fill: false,
				borderColor: 'rgb(75, 192, 192)',
				tension: 0.1
			}
		]
	});

	let options = (currTime: number): ChartOptions => ({
		plugins: {
			tooltip: {
				displayColors: false,
				callbacks: {
					label: function (tooltipItem) {
						return `Accuracy: ${Math.floor(100 * parseFloat(tooltipItem.formattedValue)) / 100}m`;
					},

					title: function (tooltipItems) {
						return tooltipItems.map((tooltipItem) => `Time: ${tooltipItem.label}s`);
					}
				}
			},
			legend: {
				display: false
			},
			title: {
				display: true,
				text: 'Accuracy Over Time'
			},
			annotation: {
				annotations: {
					nowLine: {
						type: 'line',
						borderColor: 'red',
						borderWidth: 2,
						xMin: currTime,
						xMax: currTime
					},
					averageLine: {
						type: 'line',
						borderColor: 'lightgreen',
						borderWidth: 2,
						yMin: $averageWifinderAccuracy || 0,
						yMax: $averageWifinderAccuracy || 0,
						label: {
							content: 'Average WiFinder Accuracy'
						}
					}
				}
			}
		},
		maintainAspectRatio: false,
		scales: {
			x: {
				min: 0,
				type: 'linear',
				title: {
					display: true, // Set to true to show the label
					text: 'Time since start of logs / s' // The text for your Y-axis label
				}
			},
			y: {
				type: 'linear',
				title: {
					display: true, // Set to true to show the label
					text: 'Accuracy / m' // The text for your Y-axis label
				}
			}
		}
	});

	function makeChart(ctx: HTMLCanvasElement) {
		const myChart = new Chart(ctx, { type: 'line', data }); //init the chart
		$effect(() => {
			myChart.data = data;
			myChart.update();
			const unsub = currentPlayingTimeSeconds.subscribe((v) => {
				myChart.options = options(v) as any;
				myChart.update();
			});

			return () => {
				myChart.destroy();
				unsub();
			};
		});
	}
</script>

<div class="h-120 max-w-full">
	<canvas use:makeChart class="rounded-md bg-white p-2"></canvas>
</div>
