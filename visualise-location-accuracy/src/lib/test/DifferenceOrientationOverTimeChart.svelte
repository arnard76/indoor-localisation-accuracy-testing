<script lang="ts">
	import { Chart as C, type ChartOptions } from 'chart.js';
	import { Chart } from 'chart.js/auto';
	import annotation from 'chartjs-plugin-annotation';
	import dayjs from 'dayjs';
	import { type createPlayer } from './playbackTimes';
	import { type Comparison } from './positionAccuracy';

	let {
		player,
		orientationDiffs,
		averageAccuracy
	}: {
		player: ReturnType<typeof createPlayer>;
		orientationDiffs: Comparison['diffs'];
		averageAccuracy: number;
	} = $props();

	$inspect(orientationDiffs);

	C.register(annotation);

	let data = $derived({
		labels: orientationDiffs.map(({ timestamp }) =>
			dayjs(timestamp).diff($player.startTimeForTestPreview, 'seconds')
		),
		datasets: [
			{
				data: orientationDiffs.map(({ orientationDiff }) => orientationDiff),
				fill: false,
				borderColor: 'rgb(75, 192, 192)',
				tension: 0.1
			}
		]
	});

	let options: ChartOptions = $derived({
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
				text: 'Orientation Accuracy'
			},
			annotation: {
				annotations: {
					nowLine: {
						type: 'line',
						borderColor: 'red',
						borderWidth: 2,
						xMin: $player.currentPlayingTimeSeconds,
						xMax: $player.currentPlayingTimeSeconds
					},
					averageLine: {
						type: 'line',
						borderColor: 'lightgreen',
						borderWidth: 2,
						yMin: averageAccuracy || 0,
						yMax: averageAccuracy || 0,
						label: {
							content: 'Average WiFinder Accuracy'
						}
					}
				}
			}
		},
		maintainAspectRatio: false,
		animation: false,
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
					text: 'Difference in Orientation / °' // The text for your Y-axis label
				}
			}
		}
	});

	let chartEl: HTMLCanvasElement | undefined = $state();
	let chart: Chart | undefined = $state();

	$effect(() => {
		if (!chartEl) return;

		if (!chart) {
			chart = new Chart(chartEl, { type: 'line', data, options });
		}
	});

	$effect(() => {
		if (!chart) return;

		chart.options = options;
		chart.update();
	});
</script>

<div class="h-120 max-w-full">
	<canvas bind:this={chartEl} class="rounded-md bg-white p-2"></canvas>
</div>
