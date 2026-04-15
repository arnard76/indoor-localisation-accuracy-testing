<script lang="ts">
	import { Chart as C, type ChartOptions } from 'chart.js';
	import { Chart } from 'chart.js/auto';
	import annotation from 'chartjs-plugin-annotation';
	import dayjs from 'dayjs';
	import { averageWifinderAccuracy, wiFinderLocationAccuracy } from './positionAccuracy';
	import { type createPlayer } from './playbackTimes';
	let { player }: { player: ReturnType<typeof createPlayer> } = $props();

	C.register(annotation);

	let data = {
		labels: $wiFinderLocationAccuracy.map(({ timestamp }) =>
			dayjs(timestamp).diff($player.startTimeForTestPreview, 'seconds')
		),
		datasets: [
			{
				data: $wiFinderLocationAccuracy.map(({ distanceDiff }) => distanceDiff),
				fill: false,
				borderColor: 'rgb(75, 192, 192)',
				tension: 0.1
			}
		]
	};

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
			const unsub = player.subscribe((v) => {
				myChart.options = options(v.currentPlayingTimeSeconds) as any;
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
