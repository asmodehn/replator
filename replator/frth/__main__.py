from prompt_toolkit import prompt

from replator.frth.interp import VFC

with VFC() as interp:
    while True:
        try:
            user_input = prompt(message=u'frth>',
                                history=FileHistory(os.path.join(replator_path, 'frth-history.txt')),
                                auto_suggest=AutoSuggestFromHistory(),
                                #                        completer=SQLCompleter(),
                                #                        lexer=SqlLexer,
                                )
        except KeyboardInterrupt:
            continue
        except EOFError:
            break

        interp(user_input)

        pysource = CalculatePython().transform(AST)

        # TODO : fix that in the grammar
        if not isinstance(pysource, (str,)):
            pysource = str(pysource)

        pycode = compile(pysource, '<string>', 'single')
        exec(pycode, {"__builtins__": None}, lcls)




# build/instantiate one virtual computer
VM = VFC()

# activate the VM
with VM as CPU:  # VM started

    while CPU.running:

        #user -> stream conversion is managed in host lang
        input= prompt('prpt> ')

        # stream -> exec -> stream in managed in guest lang
        output= CPU.exec(input)

        #stream -> user conversion is managed in hostlang
        print(output)
        


# SOmetimes VM is "embedded" in host language
VM = ASTConvert()
with VM as CPU:

    while CPU.running:

