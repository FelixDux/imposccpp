import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import {PlotterApp, PlotterInput, PlotterInputGroup, PlotterForm, ActionSelector} from './plotter';

function mockInputChangeHandler(event) {

}

test('Input field renders label', async () => {

    const props = {
        type: 'integer',
        range: '',
        name: 'test',
        label: 'Test',
        tooltip: 'A test field',
        value: 0,
        onChange: mockInputChangeHandler
    };

    render(<table><tbody>< PlotterInput 
        type={props.type}
        range={props.range}
        name={props.name}
        label={props.label}
        tooltip={props.tooltip}
        value={props.value}
        onChange={props.onChange}
         /></tbody></table>);

    const element = screen.getByText(props.label);

    expect(element).toBeInTheDocument();

    fireEvent.mouseOver(element);

    const tooltip = screen.getByText(props.tooltip);

    expect(tooltip).toBeInTheDocument();
});

const mockGroup = {
    name: 'My group',
    inputs: [
        {
            name: 'floater',
            range: 'positive',
            label: 'Floater',
            type: 'float',
            tooltip: 'A float field'
        },
        {
            name: 'int_field',
            range: 'non-positive',
            label: 'Int field',
            type: 'integer',
            tooltip: 'An integer field <= 0'
        },
    ],
    values: {
        'floater': 1.0,
        'int_field': -1
    }
};

test('Input group renders', async () => {
    render(< PlotterInputGroup 
        name = {mockGroup.name}
        inputs = {mockGroup.inputs}
        values = {mockGroup.values}
        onChange = {mockInputChangeHandler}
    />);

    const nameElement = screen.getByText(mockGroup.name);

    expect(nameElement).toBeInTheDocument();

    Object.entries(mockGroup.values).forEach(entry => {
        const [key, value] = entry;
        const inputElement = screen.getByDisplayValue(value);
        expect(inputElement).toBeInTheDocument();
        expect(inputElement).toHaveProperty('name', key);
    });

    const toggleButton = screen.getByRole('button');

    expect(toggleButton).toBeInTheDocument();
    expect(toggleButton.textContent).toEqual('-');

    fireEvent.click(toggleButton);
    expect(toggleButton.textContent).toEqual('+');

    Object.entries(mockGroup.values).forEach(entry => {
        const [key, value] = entry;
        const inputElement = screen.queryByDisplayValue(value);
        expect(inputElement).not.toBeInTheDocument();
    });

    fireEvent.click(toggleButton);
    expect(toggleButton.textContent).toEqual('-');

    Object.entries(mockGroup.values).forEach(entry => {
        const [key, value] = entry;
        const inputElement = screen.getByDisplayValue(value);
        expect(inputElement).toBeInTheDocument();
        expect(inputElement).toHaveProperty('name', key);
    });
});
