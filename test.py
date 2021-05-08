import requests
import concurrent.futures as cf
import time
import argparse

def main(n, type, user=1, amount=0, response=False):
    if not n or not type:
        print('Invalid arguements')
        return

    url = f'http://localhost:8000/{user}/wallet/{type}/'
    json = {'amount': amount}

    print(f'Making call: "{url}" with arguements: "{json}" {n} times')
    print()

    timer = time.time()
    with cf.ThreadPoolExecutor(max_workers=n) as executor:
        futures = [executor.submit(requests.post, url, json=json) for _ in range(n)]
        responses = [future.result() for future in futures]
    timer = time.time() - timer

    print(f'Total time taken: {timer}')
    print(f'Time taken per call: {timer / n}')

    if response:
        print('\n----Result----\n')
        for response in responses:
            print(response.json())

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', type=int, help='number of parallel calls to make')
    parser.add_argument('--type', type=str, help='type of call to make (create/credit/debit)')
    parser.add_argument('--user', type=int, nargs='?', help='user id for which to use the wallet')
    parser.add_argument('--amount', type=int, nargs='?', help='amount to credit/debit')
    parser.add_argument('--response', action='store_true', help='print the response')

    args = parser.parse_args()

    main(args.n, args.type, args.user, args.amount, args.response)
