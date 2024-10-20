$(document).ready(function() {
    // Add Rule
    $('#addRuleBtn').on('click', function() {
        const rule = $('#ruleInput').val();
        const number_of_rules = 1; // You can adjust this as needed

        $.get(`/get-rule?number_of_rules=${number_of_rules}&rule=${rule}`, function(data) {
            console.log(data);
            alert('Rule added successfully!');
        }).fail(function(err) {
            console.error(err);
            alert('Error adding rule!');
        });
    });

    // Select Rule
    $('#selectRuleBtn').on('click', function() {
        const rule_number = $('#selectRuleNumber').val();

        $.get(`/select_rule?rule_number=${rule_number}`, function(data) {
            console.log(data);
            alert('Rule selected successfully!');
        }).fail(function(err) {
            console.error(err);
            alert('Error selecting rule!');
        });
    });

    // Get Operands
    $('#getOperandsBtn').on('click', function() {
        $.get('/get_operands', function(data) {
            console.log(data);
            $('#operandsList').empty().append('<p>Operands: ' + JSON.stringify(data.list_of_operand_variables) + '</p>');
        }).fail(function(err) {
            console.error(err);
            $('#operandsList').text('Error getting operands.');
        });
    });

    // Evaluate User Data
    $('#evaluateBtn').on('click', function() {
        const userData = $('#userDataInput').val().split(',').reduce((acc, curr) => {
            const [key, value] = curr.split('=');
            acc[key.trim()] = value.trim();
            return acc;
        }, {});

        $.get(`/evaluate_user_data?${$.param(userData)}`, function(data) {
            console.log(data);
            $('#evaluationResult').text('Evaluation Result: ' + JSON.stringify(data));
        }).fail(function(err) {
            console.error(err);
            $('#evaluationResult').text('Error evaluating user data.');
        });
    });

    // Combine Rules
    $('#combineRuleBtn').on('click', function() {
        const number = $('#combineNumber').val();
        const operator = $('#combineOperator').val();
        const ruleNumbers = $('#combineRuleNumbers').val().split(',').map(num => num.trim());

        const params = {
            number: number,
            operator: operator,
        };

        ruleNumbers.forEach((ruleNumber, index) => {
            params[`rule_number`] = ruleNumber; // Append rule numbers to params
        });

        $.get('/add-rule', params, function(data) {
            console.log(data);
            $('#combinedRuleResult').text('Combined Rule: ' + JSON.stringify(data));
        }).fail(function(err) {
            console.error(err);
            $('#combinedRuleResult').text('Error combining rules.');
        });
    });
});
