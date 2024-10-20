document.getElementById('create-rule-btn').addEventListener('click', () => {
    const ruleCount = document.getElementById('rule-count').value;
    const ruleInput = document.getElementById('rule-input').value;

    fetch(`/get-rule?number_of_rules=${ruleCount}&rule=${ruleInput}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        alert('Rule saved successfully!');
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

document.getElementById('select-rule-btn').addEventListener('click', () => {
    const ruleNumber = document.getElementById('rule-number').value;

    fetch(`/select_rule?rule_number=${ruleNumber}`, {
        method: 'GET'
    })
    .then(() => {
        fetch(`/get_operands`, {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => {
            const operandSection = document.querySelector('.operands-section');
            const operandInputsDiv = document.getElementById('operand-inputs');
            operandInputsDiv.innerHTML = ''; // Clear previous inputs

            data.list_of_operand_variables.forEach(operand => {
                const inputElement = document.createElement('input');
                inputElement.setAttribute('type', 'text');
                inputElement.setAttribute('placeholder', `Enter value for ${operand}`);
                inputElement.setAttribute('id', operand);
                operandInputsDiv.appendChild(inputElement);
            });

            operandSection.style.display = 'block';
        })
        .catch(error => console.error('Error:', error));
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('evaluate-btn').addEventListener('click', () => {
    const inputs = document.querySelectorAll('#operand-inputs input');
    const params = new URLSearchParams();

    inputs.forEach(input => {
        params.append(input.id, input.value);
    });

    fetch(`/evaluate_user_data?${params.toString()}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = `Result: ${data}`;
    })
    .catch(error => {
        document.getElementById('result').innerText = 'Error evaluating rule';
        console.error('Error:', error);
    });
});
