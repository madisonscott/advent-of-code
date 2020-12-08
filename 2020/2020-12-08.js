const { exception } = require('console');
const fs = require('fs');
const path = require('path');

function parseInstructionsFromInput(input) {
    let instructionRegex = /(nop|acc|jmp) ((\+|\-)\d+)/g;

    let instructions = [];
    while (match = instructionRegex.exec(input)) {
        let [_, command, number] = match;
        instructions.push({
            command: command,
            number: parseInt(number),
        })
    }

    return instructions;
}

function runProgram(instructions, failGracefullyOnLoop = false) {
    let accumulator = 0;
    let currentLine = 0;
    let executedLines = new Set();

    while (true) {
        if (executedLines.has(currentLine)) {
            if (failGracefullyOnLoop) {
                return accumulator;
            }

            throw Exception('And in that moment, we were infinite');
        }

        if (currentLine == instructions.length) {
            return accumulator;
        }

        let {command, number} = instructions[currentLine];
        executedLines.add(currentLine);

        if (command == 'nop') {
            currentLine++;
        } else if (command == 'acc') {
            accumulator += number;
            currentLine++;
        } else if (command == 'jmp') {
            currentLine += number;
        }
    }
}

function swapCommand(command) {
    switch (command) {
        case 'nop': return 'jmp';
        case 'acc': return 'acc';
        case 'jmp': return 'nop';
        default:    throw Exception('Invalid command');
    }
}

function fixAndRunProgram(instructions) {
    for (const instruction of instructions) {
        const originalCommand = instruction.command;
        instruction.command = swapCommand(originalCommand);

        try {
            return runProgram(instructions);
        } catch {
            // these are not the droids you're looking for
        }

        instruction.command = originalCommand;
    }

    throw Exception('No valid fixes found')
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

    let instructions = parseInstructionsFromInput(input);
    console.log(runProgram(instructions, failGracefullyOnLoop = true));
    console.log(fixAndRunProgram(instructions));
}

if (require.main === module) {
    main();
}



