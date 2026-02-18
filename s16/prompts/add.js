function sum(...numbers) {
    return numbers.reduce((accumulator, current) => accumulator + current, 0)
}
const res = sum(7, 3)

console.log(res);
