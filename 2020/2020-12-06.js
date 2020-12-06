const fs = require('fs');
const path = require('path');

function parseAnswersByGroupFromInput(input) {
  let allAnswers = [];

  input.split('\n\n').forEach((group) => {
    let groupAnswers = [];

    group.split('\n').forEach((human) => {
      let humanAnswers = new Set(human.split(''));
      groupAnswers.push(humanAnswers);
    });

    allAnswers.push(groupAnswers);
  });

  return allAnswers;
}

function getNumberQuestionsThatAnyHumanAnsweredYes(groupAnswers) {
  return groupAnswers
    .reduce(
      (result, humanAnswers) => new Set([...result, ...humanAnswers]),
      new Set())
    .size;
}

function getNumberQuestionsThatAllHumanAnsweredYes(groupAnswers) {
  return groupAnswers
    .reduce(
      (result, humanAnswers) =>
        new Set([...result].filter(q => humanAnswers.has(q))),
        new Set(groupAnswers[0]))
    .size;
}

function solvePuzzle(input, accumulator) {
  let answersByGroup = parseAnswersByGroupFromInput(input);
  return answersByGroup.reduce((result, group) => result += accumulator(group), 0);
}

function main() {
  let inputFileName = `${path.basename(__filename, '.js')}.txt`;
  let inputFilePath = path.join('input', inputFileName);

  let input = '';

  try {
    input = fs.readFileSync(inputFilePath, 'utf8')
  } catch (err) {
    console.error(err)
    return;
  }

  console.log(solvePuzzle(input, getNumberQuestionsThatAnyHumanAnsweredYes));
  console.log(solvePuzzle(input, getNumberQuestionsThatAllHumanAnsweredYes));
}

if (require.main === module) {
  main();
}
