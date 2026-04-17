import type { EncodingOption } from 'fs';

export function downloadSomething(
	type: string,
	charset: EncodingOption,
	fileName: string,
	data: string
) {
	const testResultsData = `data:${type};charset=${charset},` + data;
	const downloadEl = document.createElement('a');
	downloadEl.setAttribute('href', testResultsData);
	downloadEl.setAttribute('download', fileName);
	downloadEl.click();
}
